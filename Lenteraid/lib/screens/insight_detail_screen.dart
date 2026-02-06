import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import 'package:lentera/models/mood_entry.dart';
import 'package:lentera/services/api_client.dart';
import 'package:lentera/theme.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

class InsightDetailScreen extends StatefulWidget {
  final DateTime date;
  final MoodEntry? entry;
  const InsightDetailScreen({super.key, required this.date, this.entry});

  @override
  State<InsightDetailScreen> createState() => _InsightDetailScreenState();
}

class _InsightDetailScreenState extends State<InsightDetailScreen> {
  bool _saved = false;

  String get _emoji {
    final rating = widget.entry?.moodRating ?? 3;
    switch (rating) {
      case 5:
        return '😊';
      case 4:
        return '🙂';
      case 2:
        return '😔';
      case 1:
        return '😢';
      default:
        return '😐';
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final text = context.textStyles;
    final dateLabel = DateFormat('EEEE, d MMMM yyyy', 'id_ID').format(widget.date);

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: theme.colorScheme.onSurface),
          onPressed: () => context.pop(),
        ),
        title: Text('Insight', style: text.titleLarge?.semiBold),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: AppSpacing.paddingLg,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 56,
                    height: 56,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: theme.colorScheme.tertiaryContainer,
                    ),
                    alignment: Alignment.center,
                    child: Text(_emoji, style: const TextStyle(fontSize: 28)),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(dateLabel, style: text.titleMedium?.semiBold),
                        if (widget.entry?.moodTags case final tags?
                            when tags.isNotEmpty)
                          Padding(
                            padding: const EdgeInsets.only(top: 6),
                            child: Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: tags
                                  .map((t) => Chip(
                                        label: Text(t),
                                      ))
                                  .toList(),
                            ),
                          ),
                      ],
                    ),
                  )
                ],
              ),
              const SizedBox(height: AppSpacing.xl),

              Text('Catatan Jurnal', style: text.titleMedium?.semiBold),
              const SizedBox(height: 8),
              Container(
                width: double.infinity,
                padding: AppSpacing.paddingMd,
                decoration: BoxDecoration(
                  color: theme.colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(AppRadius.lg),
                ),
                child: Text(
                  widget.entry?.journalText?.isNotEmpty == true
                      ? widget.entry!.journalText!
                      : 'Belum ada catatan untuk tanggal ini.',
                  style: text.bodyMedium?.withColor(theme.colorScheme.onSurface),
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              _InsightAISection(
                entry: widget.entry,
                onSave: () {
                  setState(() => _saved = !_saved);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text(_saved ? 'Insight disimpan' : 'Insight dibatalkan')),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InsightAISection extends StatefulWidget {
  final MoodEntry? entry;
  final VoidCallback onSave;
  const _InsightAISection({this.entry, required this.onSave});

  @override
  State<_InsightAISection> createState() => _InsightAISectionState();
}

class _InsightAISectionState extends State<_InsightAISection> {
  String? _analysis;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchAnalysis();
  }

  Future<void> _fetchAnalysis() async {
    if (widget.entry == null) return;
    
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final apiClient = ApiClient();
      final result = await apiClient.analyzeMood(
        moodRating: widget.entry!.moodRating,
        emotions: widget.entry!.moodTags,
        journal: widget.entry!.journalText,
      );
      
      setState(() {
        _analysis = result['analysis'] ?? result['message'] ?? 'Gagal mendapatkan analisis.';
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Maaf, terjadi kesalahan saat menghubungi AI.';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final text = context.textStyles;

    return Container(
      width: double.infinity,
      padding: AppSpacing.paddingLg,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppRadius.xl),
        border: Border.all(color: theme.colorScheme.outline.withValues(alpha: 0.18)),
        gradient: LinearGradient(
          colors: [
            theme.colorScheme.tertiaryContainer.withValues(alpha: 0.5),
            theme.colorScheme.secondaryContainer.withValues(alpha: 0.3),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Text('🤖', style: TextStyle(fontSize: 22)),
              const SizedBox(width: 8),
              Text('Insight dari Lentera AI', style: text.titleMedium?.semiBold),
              if (_loading)
                const Padding(
                  padding: EdgeInsets.only(left: 12),
                  child: SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
          
          if (_loading)
             Text(
              'Sedang menganalisis catatanmu...',
              style: text.bodyMedium?.copyWith(fontStyle: FontStyle.italic).withColor(theme.colorScheme.onSurfaceVariant),
            )
          else if (_error != null)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(_error!, style: text.bodyMedium?.withColor(theme.colorScheme.error)),
                TextButton(
                  onPressed: _fetchAnalysis,
                  child: const Text('Coba Lagi'),
                ),
              ],
            )
          else if (_analysis != null)
            MarkdownBody(
              data: _analysis!,
              styleSheet: MarkdownStyleSheet(
                p: text.bodyMedium,
                strong: text.bodyMedium?.bold,
                listBullet: text.bodyMedium,
              ),
            )
          else
            Text(
              'Belum ada insight. Coba buat jurnal yang lebih detail!',
              style: text.bodyMedium?.withColor(theme.colorScheme.onSurfaceVariant),
            ),

          const SizedBox(height: AppSpacing.lg),
          if (!_loading && _analysis != null)
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: widget.onSave,
                style: ElevatedButton.styleFrom(
                  backgroundColor: theme.colorScheme.primary,
                  foregroundColor: theme.colorScheme.onPrimary,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(AppRadius.lg),
                  ),
                  elevation: 0,
                ),
                child: Text('Simpan Insight', style: text.labelLarge?.withColor(theme.colorScheme.onPrimary)),
              ),
            )
        ],
      ),
    );
  }
}
