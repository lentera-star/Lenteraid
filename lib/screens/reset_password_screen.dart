import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:lentera/supabase/supabase_config.dart';
import 'package:lentera/theme.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class ResetPasswordScreen extends StatefulWidget {
  const ResetPasswordScreen({super.key});

  @override
  State<ResetPasswordScreen> createState() => _ResetPasswordScreenState();
}

class _ResetPasswordScreenState extends State<ResetPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _passController = TextEditingController();
  final _confirmController = TextEditingController();
  bool _submitting = false;
  bool _obscure1 = true;
  bool _obscure2 = true;
  String? _linkError;

  @override
  void initState() {
    super.initState();
    // If Supabase redirected with an error (e.g., otp_expired), surface it.
    final uri = Uri.base; // works on web; on mobile it's harmless
    final error = uri.queryParameters['error_description'] ?? uri.queryParameters['error'];
    if (error != null && error.isNotEmpty) {
      _linkError = Uri.decodeComponent(error);
    }
  }

  @override
  void dispose() {
    _passController.dispose();
    _confirmController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _submitting = true);
    try {
      await SupabaseConfig.auth.updateUser(UserAttributes(password: _passController.text.trim()));
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Password berhasil diperbarui. Silakan masuk.')));
      context.go('/login');
    } catch (e) {
      debugPrint('Failed to update password: $e');
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gagal memperbarui password: $e')));
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colors = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Atur Ulang Password'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          color: colors.onSurface,
          onPressed: () => context.pop(),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: AppSpacing.paddingLg,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 12),
                Icon(Icons.lock_outline, size: 72, color: colors.primary),
                const SizedBox(height: 16),
                Text('Buat Password Baru', style: theme.textTheme.titleLarge?.semiBold, textAlign: TextAlign.center),
                const SizedBox(height: 8),
                Text('Masukkan password baru Anda di bawah ini.', textAlign: TextAlign.center, style: theme.textTheme.bodyMedium?.withColor(colors.onSurface.withValues(alpha: 0.7))),
                if (_linkError != null) ...[
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: colors.errorContainer,
                      borderRadius: BorderRadius.circular(AppRadius.md),
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(Icons.error_outline, color: colors.error),
                        const SizedBox(width: 8),
                        Expanded(child: Text(_linkError!, style: theme.textTheme.bodySmall?.withColor(colors.onErrorContainer))),
                      ],
                    ),
                  ),
                ],
                const SizedBox(height: 24),
                TextFormField(
                  controller: _passController,
                  obscureText: _obscure1,
                  decoration: InputDecoration(
                    labelText: 'Password baru',
                    prefixIcon: const Icon(Icons.password, color: Colors.blue),
                    suffixIcon: IconButton(
                      icon: Icon(_obscure1 ? Icons.visibility : Icons.visibility_off, color: Colors.blue),
                      onPressed: () => setState(() => _obscure1 = !_obscure1),
                    ),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(AppRadius.md)),
                  ),
                  validator: (v) {
                    final t = (v ?? '').trim();
                    if (t.length < 8) return 'Minimal 8 karakter';
                    return null;
                  },
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _confirmController,
                  obscureText: _obscure2,
                  decoration: InputDecoration(
                    labelText: 'Konfirmasi password',
                    prefixIcon: const Icon(Icons.check_circle_outline, color: Colors.blue),
                    suffixIcon: IconButton(
                      icon: Icon(_obscure2 ? Icons.visibility : Icons.visibility_off, color: Colors.blue),
                      onPressed: () => setState(() => _obscure2 = !_obscure2),
                    ),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(AppRadius.md)),
                  ),
                  validator: (v) {
                    final t = (v ?? '').trim();
                    if (t != _passController.text.trim()) return 'Tidak cocok dengan password baru';
                    return null;
                  },
                ),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: _submitting ? null : _submit,
                  style: FilledButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 14)),
                  icon: _submitting
                      ? const SizedBox(height: 18, width: 18, child: CircularProgressIndicator(strokeWidth: 2))
                      : const Icon(Icons.save_outlined, color: Colors.white),
                  label: Text(_submitting ? 'Menyimpan...' : 'Simpan Password', style: theme.textTheme.labelLarge?.withColor(colors.onPrimary)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
