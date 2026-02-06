import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:lentera/supabase/supabase_config.dart';

/// Lightweight local gamification state with Supabase backend sync.
/// Stores: koin, xp, level, streak, lastCheckinDate, dailyTarget.
class GamificationService {
  // Singleton
  GamificationService._();
  static final GamificationService _instance = GamificationService._();
  factory GamificationService() => _instance;

  // Notifies listeners when gamification state changes
  final ValueNotifier<int> tick = ValueNotifier<int>(0);
  void _notify() {
    try {
      tick.value = tick.value + 1;
    } catch (e) {
      debugPrint('GamificationService._notify error: $e');
    }
  }

  // Keys
  static const _koinKey = 'gf_koin_balance';
  static const _xpKey = 'gf_xp_points';
  static const _levelKey = 'gf_level';
  static const _streakKey = 'gf_streak_days';
  static const _lastCheckinKey = 'gf_last_checkin_iso';
  static const _dailyTargetKey = 'gf_daily_target';

  // Defaults
  static const int _defaultKoin = 0;
  static const int _defaultXp = 0;
  static const int _defaultLevel = 1;
  static const int _defaultStreak = 0;
  static const int _defaultDailyTarget = 1;

  // Rewards
  static const int _checkinKoinReward = 10;
  static const int _checkinXpReward = 20;

  bool _isSyncing = false;

  /// Load from Supabase and update local cache
  Future<void> _syncFromBackend() async {
    final user = Supabase.instance.client.auth.currentUser;
    if (user == null) return;
    if (_isSyncing) return;

    _isSyncing = true;
    try {
      final prefs = await SharedPreferences.getInstance();
      final response = await Supabase.instance.client
          .from('user_gamification')
          .select()
          .eq('user_id', user.id)
          .maybeSingle();

      if (response != null) {
        // Update local cache from backend
        await prefs.setInt(_koinKey, response['koin'] ?? _defaultKoin);
        await prefs.setInt(_xpKey, response['xp'] ?? _defaultXp);
        await prefs.setInt(_levelKey, response['level'] ?? _defaultLevel);
        await prefs.setInt(_streakKey, response['streak_days'] ?? _defaultStreak);
        
        if (response['last_checkin_date'] != null) {
          await prefs.setString(_lastCheckinKey, response['last_checkin_date']);
        }
        
        debugPrint('☁️ [GamificationService] Synced FROM backend: K=${response['koin']} S=${response['streak_days']}');
        _notify();
      } else {
        // If no record exists, create one with current local data
        await _syncToBackend();
      }
    } catch (e) {
      debugPrint('GamificationService._syncFromBackend error: $e');
    } finally {
      _isSyncing = false;
    }
  }

  /// Save local cache to Supabase
  Future<void> _syncToBackend() async {
    final user = Supabase.instance.client.auth.currentUser;
    if (user == null) return;

    try {
      final prefs = await SharedPreferences.getInstance();
      final koin = prefs.getInt(_koinKey) ?? _defaultKoin;
      final xp = prefs.getInt(_xpKey) ?? _defaultXp;
      final level = prefs.getInt(_levelKey) ?? _defaultLevel;
      final streak = prefs.getInt(_streakKey) ?? _defaultStreak;
      final lastIso = prefs.getString(_lastCheckinKey);

      final data = {
        'user_id': user.id,
        'koin': koin,
        'xp': xp,
        'level': level,
        'streak_days': streak,
        'last_checkin_date': lastIso != null ? lastIso.split('T').first : null, // Send YYYY-MM-DD only
        'updated_at': DateTime.now().toIso8601String(),
      };

      await Supabase.instance.client
          .from('user_gamification')
          .upsert(data);
      
      debugPrint('☁️ [GamificationService] Synced TO backend: K=$koin S=$streak');
    } catch (e) {
      debugPrint('GamificationService._syncToBackend error: $e');
    }
  }

  Future<GamificationSummary> getSummary() async {
    try {
      // Trigger background sync, but don't await to keep UI snappy
      _syncFromBackend();

      final prefs = await SharedPreferences.getInstance();
      final koin = prefs.getInt(_koinKey) ?? _defaultKoin;
      final xp = prefs.getInt(_xpKey) ?? _defaultXp;
      final level = prefs.getInt(_levelKey) ?? _defaultLevel;
      final streak = prefs.getInt(_streakKey) ?? _defaultStreak;
      final dailyTarget = prefs.getInt(_dailyTargetKey) ?? _defaultDailyTarget;
      final lastIso = prefs.getString(_lastCheckinKey);
      final lastDate = lastIso != null && lastIso.isNotEmpty ? DateTime.tryParse(lastIso) : null;

      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);
      final doneToday = lastDate != null &&
          lastDate.year == today.year && lastDate.month == today.month && lastDate.day == today.day;

      final xpCycle = 100;
      final xpProgress = (xp % xpCycle) / xpCycle;

      return GamificationSummary(
        koin: koin,
        xp: xp,
        level: level,
        streak: streak,
        dailyTarget: dailyTarget,
        todayProgress: doneToday ? 1 : 0,
        xpProgress: xpProgress.clamp(0.0, 1.0),
      );
    } catch (e) {
      debugPrint('GamificationService.getSummary error: $e');
      return GamificationSummary(
        koin: _defaultKoin,
        xp: _defaultXp,
        level: _defaultLevel,
        streak: _defaultStreak,
        dailyTarget: _defaultDailyTarget,
        todayProgress: 0,
        xpProgress: 0,
      );
    }
  }

  Future<void> setDailyTarget(int target) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setInt(_dailyTargetKey, target.clamp(1, 10));
    } catch (e) {
      debugPrint('GamificationService.setDailyTarget error: $e');
    }
  }

  /// Increase/decrease koin balance by [delta].
  Future<int> addKoin(int delta) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final current = prefs.getInt(_koinKey) ?? _defaultKoin;
      final next = (current + delta).clamp(0, 1 << 30);
      await prefs.setInt(_koinKey, next);
      
      debugPrint('💰 [GamificationService] addKoin: $current → $next (delta: $delta)');
      
      _notify(); // Update UI immediately
      _syncToBackend(); // Sync to DB in background
      
      return next;
    } catch (e) {
      debugPrint('GamificationService.addKoin error: $e');
      return _defaultKoin;
    }
  }

  /// Marks today's daily check-in once and rewards koin/xp.
  Future<bool> markDailyCheckin({int? koinReward, int? xpReward}) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);
      final lastIso = prefs.getString(_lastCheckinKey);
      final lastDate = lastIso != null && lastIso.isNotEmpty ? DateTime.tryParse(lastIso) : null;

      final alreadyDone = lastDate != null &&
          lastDate.year == today.year && lastDate.month == today.month && lastDate.day == today.day;
      if (alreadyDone) {
        debugPrint('✅ [GamificationService] Already checked in today');
        return false;
      }

      // Streak
      int streak = prefs.getInt(_streakKey) ?? _defaultStreak;
      if (lastDate != null) {
        final yest = today.subtract(const Duration(days: 1));
        final wasYesterday = lastDate.year == yest.year && lastDate.month == yest.month && lastDate.day == yest.day;
        streak = wasYesterday ? streak + 1 : 1;
        debugPrint('🔥 [GamificationService] Streak updated: $streak');
      } else {
        streak = 1;
        debugPrint('🔥 [GamificationService] First streak day!');
      }

      // Koin & XP
      final rewardKoin = koinReward ?? _checkinKoinReward;
      final rewardXp = xpReward ?? _checkinXpReward;

      int koin = prefs.getInt(_koinKey) ?? _defaultKoin;
      int xp = prefs.getInt(_xpKey) ?? _defaultXp;
      int level = prefs.getInt(_levelKey) ?? _defaultLevel;

      koin += rewardKoin;
      xp += rewardXp;

      while (xp >= 100) {
        xp -= 100;
        level += 1;
      }

      await prefs.setInt(_koinKey, koin);
      await prefs.setInt(_xpKey, xp);
      await prefs.setInt(_levelKey, level);
      await prefs.setInt(_streakKey, streak);
      await prefs.setString(_lastCheckinKey, today.toIso8601String());

      debugPrint('💰 [GamificationService] Rewards granted: $rewardKoin Coins');
      
      _notify(); // Update UI
      await _syncToBackend(); // Sync to DB
      
      return true;
    } catch (e) {
      debugPrint('GamificationService.markDailyCheckin error: $e');
      return false;
    }
  }
}

class GamificationSummary {
  final int koin;
  final int xp;
  final int level;
  final int streak;
  final int dailyTarget;
  final int todayProgress;
  final double xpProgress;

  const GamificationSummary({
    required this.koin,
    required this.xp,
    required this.level,
    required this.streak,
    required this.dailyTarget,
    required this.todayProgress,
    required this.xpProgress,
  });
}
