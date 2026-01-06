import 'dart:ui';

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:lentera/theme.dart';

/// A premium consent item card with a custom checkbox, title, description,
/// and optional link. Designed for dark-mode backgrounds with glass effect.
class ConsentItemCard extends StatelessWidget {
  final bool checked;
  final ValueChanged<bool> onChanged;
  final String title;
  final String description;
  final String? linkText;
  final VoidCallback? onLinkTap;
  final bool highlighted;

  const ConsentItemCard({
    super.key,
    required this.checked,
    required this.onChanged,
    required this.title,
    required this.description,
    this.linkText,
    this.onLinkTap,
    this.highlighted = false,
  });

  @override
  Widget build(BuildContext context) {
    final consent = Theme.of(context).extension<ConsentTheme>()!;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final Color bgColor = highlighted
        ? consent.highlightBg
        : (isDark ? consent.itemBg : consent.itemBg);

    return GestureDetector(
      onTap: () => onChanged(!checked),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeInOut,
        child: ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: BackdropFilter(
            filter: ImageFilter.blur(
                sigmaX: highlighted ? 0 : 8, sigmaY: highlighted ? 0 : 8),
            child: Container(
              decoration: BoxDecoration(
                color: bgColor.withValues(
                    alpha: highlighted ? 1 : (isDark ? 0.18 : 1)),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: checked ? consent.purple : consent.purpleBorder.withValues(alpha: 0.3),
                  width: checked ? (highlighted ? 2.5 : 2) : 1,
                ),
              ),
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _CheckboxBox(
                    checked: checked,
                    color: consent.purple,
                    highlighted: highlighted,
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          title,
                          style: (context.textStyles.titleMedium ??
                                  const TextStyle())
                              .bold
                              .withColor(consent.elevatedOnSurface),
                        ),
                        const SizedBox(height: 6),
                        RichText(
                          text: TextSpan(
                            style: (context.textStyles.bodyMedium ??
                                    const TextStyle())
                                .withColor(consent.elevatedOnSurface
                                    .withValues(alpha: 0.85)),
                            children: [
                              TextSpan(text: description),
                              if (linkText != null && onLinkTap != null) ...[
                                const TextSpan(text: ' '),
                                TextSpan(
                                  text: linkText!,
                                  style: TextStyle(
                                    color: consent.purple,
                                    fontWeight: FontWeight.w500,
                                    decoration: TextDecoration.underline,
                                    decorationColor: consent.purple,
                                  ),
                                  recognizer: TapGestureRecognizer()
                                    ..onTap = onLinkTap,
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _CheckboxBox extends StatelessWidget {
  final bool checked;
  final Color color;
  final bool highlighted;

  const _CheckboxBox({
    required this.checked,
    required this.color,
    this.highlighted = false,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      curve: Curves.easeInOut,
      width: 24,
      height: 24,
      decoration: BoxDecoration(
        color: checked ? color : Colors.transparent,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(
          color: checked ? color : color.withValues(alpha: 0.5),
          width: 2,
        ),
      ),
      alignment: Alignment.center,
      child: AnimatedScale(
        duration: const Duration(milliseconds: 150),
        scale: checked ? 1.0 : 0.0,
        child: Icon(
          highlighted ? Icons.star : Icons.check,
          color: Colors.white,
          size: 16,
        ),
      ),
    );
  }
}
