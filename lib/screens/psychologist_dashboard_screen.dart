import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lentera/theme.dart';

class PsychologistDashboardScreen extends StatefulWidget {
  const PsychologistDashboardScreen({super.key});

  @override
  State<PsychologistDashboardScreen> createState() => _PsychologistDashboardScreenState();
}

class _PsychologistDashboardScreenState extends State<PsychologistDashboardScreen> {
  bool _isOnline = true;
  
  // Mock Data for Demo
  final List<Map<String, dynamic>> _upcomingSessions = [
    {
      'time': '10:00',
      'patient': 'Budi Santoso',
      'topic': 'Kecemasan Karir',
      'status': 'Confirmed',
      'type': 'Video Call'
    },
    {
      'time': '13:30',
      'patient': 'Siti Aminah',
      'topic': 'Masalah Keluarga',
      'status': 'Confirmed',
      'type': 'Chat'
    },
    {
      'time': '15:00',
      'patient': 'Rudi H',
      'topic': 'Depresi Ringan',
      'status': 'Pending',
      'type': 'Voice Call'
    },
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final branding = theme.extension<BrandingColors>() ?? BrandingColors.light;

    return Scaffold(
      backgroundColor: branding.lightGreyBg,
      appBar: AppBar(
        title: const Text('Partner Dashboard'),
        backgroundColor: Colors.white,
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_none),
            onPressed: () {},
          ),
          const SizedBox(width: 8),
          CircleAvatar(
            backgroundColor: branding.lightTealBg,
            child: Text('dr', style: TextStyle(color: branding.deepTeal)),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 1. Status Toggle Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: _isOnline ? branding.deepTeal : Colors.grey[400],
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: (_isOnline ? branding.deepTeal : Colors.grey).withOpacity(0.3),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  )
                ],
              ),
              child: Row(
                children: [
                   Container(
                     padding: const EdgeInsets.all(10),
                     decoration: BoxDecoration(
                       color: Colors.white.withOpacity(0.2),
                       shape: BoxShape.circle,
                     ),
                     child: const Icon(Icons.power_settings_new, color: Colors.white, size: 28),
                   ),
                   const SizedBox(width: 16),
                   Expanded(
                     child: Column(
                       crossAxisAlignment: CrossAxisAlignment.start,
                       children: [
                         Text(
                           _isOnline ? 'Status: ONLINE' : 'Status: OFFLINE',
                           style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                         ),
                         const SizedBox(height: 4),
                         Text(
                           _isOnline ? 'Anda terlihat oleh pasien' : 'Anda tidak menerima booking baru',
                           style: TextStyle(color: Colors.white.withOpacity(0.9), fontSize: 13),
                         ),
                       ],
                     ),
                   ),
                   Switch(
                     value: _isOnline,
                     onChanged: (val) => setState(() => _isOnline = val),
                     activeColor: Colors.white,
                     activeTrackColor: Colors.tealAccent,
                   ),
                ],
              ),
            ),
            
            const SizedBox(height: 24),

            // 2. Statistics Row
            Row(
              children: [
                _buildStatCard(theme, 'Pasien Hari Ini', '3', Icons.people_outline, Colors.blue),
                const SizedBox(width: 12),
                _buildStatCard(theme, 'Pendapatan', 'Rp 750rb', Icons.account_balance_wallet_outlined, Colors.orange),
              ],
            ),

            const SizedBox(height: 24),

            // 3. Upcoming Schedule
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Jadwal Hari Ini',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
                ),
                TextButton(onPressed: (){}, child: const Text('Lihat Semua'))
              ],
            ),
            const SizedBox(height: 8),
            
            ..._upcomingSessions.map((session) => _buildSessionCard(theme, session)),

            const SizedBox(height: 24),
            // 4. Recent Reviews
            Text(
                  'Ulasan Terbaru',
                  style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.grey.shade200),
              ),
              child: Column(
                children: [
                  Row(
                    children: [
                      const Icon(Icons.star, color: Colors.amber, size: 20),
                      const Icon(Icons.star, color: Colors.amber, size: 20),
                      const Icon(Icons.star, color: Colors.amber, size: 20),
                      const Icon(Icons.star, color: Colors.amber, size: 20),
                      const Icon(Icons.star, color: Colors.amber, size: 20),
                      const SizedBox(width: 8),
                      Text('5.0', style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    '"Dokternya sangat ramah dan mendengarkan dengan baik. Solusi yang diberikan sangat membantu saya."',
                    style: TextStyle(fontStyle: FontStyle.italic, color: Colors.black54),
                  ),
                  const SizedBox(height: 8),
                  const Align(
                    alignment: Alignment.centerRight,
                    child: Text('- Anonim, 2 jam lalu', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(ThemeData theme, String label, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey.shade200),
          boxShadow: [
             BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 8, offset: const Offset(0, 2))
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 28),
            const SizedBox(height: 12),
            Text(value, style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(label, style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildSessionCard(ThemeData theme, Map<String, dynamic> data) {
    final isConfirmed = data['status'] == 'Confirmed';
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border(
           left: BorderSide(
            color: isConfirmed ? Colors.green : Colors.orange,
            width: 4,
          ),
        ),
        boxShadow: [
           BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 4, offset: const Offset(0, 2))
        ],
      ),
      child: Row(
        children: [
          Column(
            children: [
              Text(
                data['time'],
                style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(data['type'], style: const TextStyle(fontSize: 10, color: Colors.grey)),
              ),
            ],
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(data['patient'], style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.bold)),
                const SizedBox(height: 2),
                Text('Topik: ${data['topic']}', style: theme.textTheme.bodySmall?.copyWith(color: Colors.grey.shade600)),
              ],
            ),
          ),
          if (!isConfirmed)
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.orange,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                minimumSize: const Size(60, 32),
              ),
              child: const Text('Acc'),
            )
          else
            const Icon(Icons.video_call, color: Colors.green),
        ],
      ),
    );
  }
}