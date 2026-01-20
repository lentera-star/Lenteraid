import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lentera/components/consent_item_card.dart';
import 'package:lentera/nav.dart';
import 'package:lentera/theme.dart';

class ConsentScreen extends StatefulWidget {
  const ConsentScreen({super.key});

  @override
  State<ConsentScreen> createState() => _ConsentScreenState();
}

class _ConsentScreenState extends State<ConsentScreen>
    with SingleTickerProviderStateMixin {
  // Checkbox states
  bool _acceptTerms = false;
  bool _acceptPrivacy = false;
  bool _acceptDataUsage = false;
  bool _understandLimitations = false;
  bool _confirmAge = false;

  // Animation controller for entrance
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();

    // Initialize entrance animations
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeIn),
    );

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  // Check if all required checkboxes are checked
  bool get _allChecked =>
      _acceptTerms &&
      _acceptPrivacy &&
      _acceptDataUsage &&
      _understandLimitations &&
      _confirmAge;

  void _onAccept() {
    if (_allChecked) {
      context.go(AppRoutes.home);
    }
  }

  void _onDecline() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Keluar dari Aplikasi?'),
        content: const Text(
          'Anda harus menyetujui syarat & ketentuan untuk menggunakan LENTERA.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Kembali'),
          ),
          TextButton(
            onPressed: () => context.go(AppRoutes.login),
            child: const Text(
              'Keluar',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );
  }

  void _showTermsDialog(String title, String content) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Text(title),
        content: SingleChildScrollView(
          child: Text(content),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Tutup'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    final size = MediaQuery.of(context).size;

    return Scaffold(
      body: Stack(
        children: [
          // Background gradient & subtle noise overlay
          Container(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [consent.bgTop, consent.bgBottom],
              ),
            ),
          ),
          // Subtle frosted noise using blur layer
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
              child: Container(color: Colors.transparent),
            ),
          ),

          FadeTransition(
            opacity: _fadeAnimation,
            child: SlideTransition(
              position: _slideAnimation,
              child: SafeArea(
                child: Column(
                  children: [
                    const SizedBox(height: 12),
                    _Header(),
                    const SizedBox(height: AppSpacing.lg),
                    Expanded(
                      child: SingleChildScrollView(
                        padding: const EdgeInsets.symmetric(horizontal: 20),
                        child: Column(
                          children: [
                            _GlassCard(
                              child: _buildCardContent(),
                            ),
                            SizedBox(height: size.height * 0.15),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // Bottom action section
          Align(
            alignment: Alignment.bottomCenter,
            child: _buildBottomActionBar(),
          ),
        ],
      ),
    );
  }

  Widget _buildCardContent() {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Syarat & Ketentuan',
          style: (context.textStyles.headlineSmall ?? const TextStyle())
              .bold
              .withColor(consent.elevatedOnSurface),
        ),
        const SizedBox(height: 8),
        Text(
          'Selamat datang di LENTERA! Silakan baca dan setujui hal-hal berikut sebelum melanjutkan:',
          style: (context.textStyles.bodyMedium ?? const TextStyle())
              .withColor(consent.elevatedOnSurface.withValues(alpha: 0.7)),
        ),
        const SizedBox(height: AppSpacing.lg),

        // Items
        ConsentItemCard(
          checked: _acceptTerms,
          onChanged: (val) => setState(() => _acceptTerms = val),
          title: 'Syarat & Ketentuan Penggunaan',
          description:
              'Saya telah membaca dan memahami syarat penggunaan aplikasi LENTERA.',
          linkText: 'Baca selengkapnya',
          onLinkTap: () => _showTermsDialog(
            'Syarat & Ketentuan',
            _getTermsContent('terms'),
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        ConsentItemCard(
          checked: _acceptPrivacy,
          onChanged: (val) => setState(() => _acceptPrivacy = val),
          title: 'Kebijakan Privasi',
          description:
              'Saya menyetujui pengumpulan dan penggunaan data pribadi sesuai kebijakan privasi.',
          linkText: 'Baca kebijakan privasi',
          onLinkTap: () => _showTermsDialog(
            'Kebijakan Privasi',
            _getTermsContent('privacy'),
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        ConsentItemCard(
          checked: _acceptDataUsage,
          onChanged: (val) => setState(() => _acceptDataUsage = val),
          title: 'Penggunaan Data',
          description:
              'Data percakapan akan digunakan untuk meningkatkan layanan dan disimpan sesuai UU PDP Indonesia.',
          linkText: 'Detail penggunaan data',
          onLinkTap: () => _showTermsDialog(
            'Penggunaan Data',
            _getTermsContent('data'),
          ),
        ),
        const SizedBox(height: AppSpacing.md),
        ConsentItemCard(
          checked: _understandLimitations,
          onChanged: (val) => setState(() => _understandLimitations = val),
          highlighted: true,
          title: 'Batasan Layanan AI',
          description:
              'Saya memahami bahwa LENTERA adalah AI pendukung, bukan pengganti psikolog profesional.',
        ),
        const SizedBox(height: AppSpacing.md),
        ConsentItemCard(
          checked: _confirmAge,
          onChanged: (val) => setState(() => _confirmAge = val),
          title: 'Konfirmasi Usia',
          description:
              'Saya berusia 18 tahun atau lebih, atau memiliki izin orang tua/wali.',
        ),
      ],
    );
  }

  Widget _buildBottomActionBar() {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      decoration: BoxDecoration(
        color: consent.elevatedSurface,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(30),
          topRight: Radius.circular(30),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.15),
            blurRadius: 24,
            offset: const Offset(0, -8),
          ),
        ],
      ),
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 20),
      child: SafeArea(
        top: false,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Primary CTA
            AnimatedOpacity(
              duration: const Duration(milliseconds: 300),
              opacity: _allChecked ? 1.0 : 0.5,
              child: DecoratedBox(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: _allChecked
                        ? [consent.purple, consent.purpleBorder]
                        : [
                            consent.purple.withValues(alpha: 0.5),
                            consent.purpleBorder.withValues(alpha: 0.5)
                          ],
                    begin: Alignment.centerLeft,
                    end: Alignment.centerRight,
                  ),
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: _allChecked
                      ? [
                          BoxShadow(
                            color: consent.purple.withValues(alpha: 0.5),
                            blurRadius: 18,
                            offset: const Offset(0, 10),
                          )
                        ]
                      : [],
                ),
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    borderRadius: BorderRadius.circular(16),
                    onTap: _allChecked ? _onAccept : null,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(
                          vertical: 16, horizontal: 16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'Setuju & Lanjutkan',
                            style: (context.textStyles.titleMedium ??
                                    const TextStyle())
                                .bold
                                .withColor(
                                    Theme.of(context).colorScheme.onPrimary),
                          ),
                          const SizedBox(width: 8),
                          Icon(Icons.arrow_forward_rounded,
                              color:
                                  Theme.of(context).colorScheme.onPrimary),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 10),
            TextButton(
              onPressed: _onDecline,
              child: Text(
                'Tolak & Keluar',
                style: (context.textStyles.labelLarge ?? const TextStyle())
                    .withColor(Theme.of(context).colorScheme.onSurfaceVariant),
              ),
            )
          ],
        ),
      ),
    );
  }

  String _getTermsContent(String type) {
    switch (type) {
      case 'terms':
        return '''
SYARAT & KETENTUAN LENTERA

1. PENERIMAAN SYARAT
Dengan menggunakan aplikasi LENTERA, Anda menyetujui untuk terikat dengan syarat dan ketentuan ini.

2. LAYANAN
LENTERA adalah asisten AI untuk dukungan kesehatan mental. BUKAN pengganti terapi profesional.

3. PENGGUNAAN YANG DILARANG
- Tidak untuk diagnosis medis
- Tidak untuk krisis darurat (hubungi 119 ext 8 atau 1500-454)
- Tidak untuk anak di bawah 18 tahun tanpa pengawasan

4. BATASAN TANGGUNG JAWAB
LENTERA tidak bertanggung jawab atas keputusan yang dibuat berdasarkan saran AI.

5. PERUBAHAN LAYANAN
Kami dapat mengubah layanan sewaktu-waktu.
        ''';

      case 'privacy':
        return '''
KEBIJAKAN PRIVASI LENTERA

1. DATA YANG DIKUMPULKAN
- Percakapan (terenkripsi)
- Metadata (waktu, durasi)
- Data perangkat (untuk debugging)

2. PENGGUNAAN DATA
- Meningkatkan layanan AI
- Analisis agregat (tanpa identitas)
- Riset kesehatan mental (anonymized)

3. KEAMANAN
- Enkripsi end-to-end
- Server di Indonesia
- Sesuai UU PDP No. 27 Tahun 2022

4. HAK ANDA
- Akses data Anda
- Hapus data Anda
- Opt-out dari riset
        ''';

      case 'data':
        return '''
PENGGUNAAN DATA LENTERA

1. DATA PERCAKAPAN
- Disimpan terenkripsi
- Digunakan untuk training AI (anonymized)
- Dapat dihapus kapan saja

2. DATA SUARA
- Diproses lokal (tidak disimpan permanen)
- Transkripsi disimpan sebagai teks

3. KEPATUHAN
- UU PDP Indonesia (No. 27/2022)
- GDPR-compliant
- ISO 27001 security standards
        ''';

      default:
        return 'Konten tidak tersedia.';
    }
  }
}

class _Header extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Column(
        children: [
          Container(
            width: 84,
            height: 84,
            decoration: BoxDecoration(
              color: Theme.of(context)
                  .extension<ConsentTheme>()!
                  .elevatedSurface,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.2),
                  blurRadius: 18,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Icon(Icons.psychology_alt, color: consent.purple, size: 40),
          ),
          const SizedBox(height: 16),
          Text(
            'LENTERA',
            style: (context.textStyles.headlineLarge ?? const TextStyle())
                .bold
                .withColor(Theme.of(context).colorScheme.onSurface),
          ),
          const SizedBox(height: 6),
          Text(
            'Pendamping Kesehatan Mental Anda',
            style: (context.textStyles.bodyMedium ?? const TextStyle())
                .withColor(Theme.of(context)
                    .colorScheme
                    .onSurface
                    .withValues(alpha: 0.85)),
          ),
        ],
      ),
    );
  }
}

class _GlassCard extends StatelessWidget {
  final Widget child;
  const _GlassCard({required this.child});

  @override
  Widget build(BuildContext context) {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    return ClipRRect(
      borderRadius: BorderRadius.circular(30),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
        child: Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: consent.elevatedSurface.withValues(alpha: 0.92),
            borderRadius: BorderRadius.circular(30),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.15),
                blurRadius: 24,
                offset: const Offset(0, 18),
              )
            ],
          ),
          padding: const EdgeInsets.all(22),
          child: child,
        ),
      ),
    );
  }
}
