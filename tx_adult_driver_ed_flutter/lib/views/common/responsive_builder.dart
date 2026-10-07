import 'package:flutter/material.dart';

enum DeviceType { mobile, tablet, desktop }

class ResponsiveBuilder extends StatelessWidget {
  final Widget Function(BuildContext context, BoxConstraints constraints, DeviceType deviceType) builder;

  const ResponsiveBuilder({super.key, required this.builder});

  static DeviceType getDeviceType(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    if (width < 600) return DeviceType.mobile;
    if (width < 1024) return DeviceType.tablet;
    return DeviceType.desktop;
  }

  static bool isMobile(BuildContext context) => getDeviceType(context) == DeviceType.mobile;
  static bool isTablet(BuildContext context) => getDeviceType(context) == DeviceType.tablet;
  static bool isDesktop(BuildContext context) => getDeviceType(context) == DeviceType.desktop;

  static double getHorizontalPadding(BuildContext context) {
    if (isMobile(context)) return 16.0;
    if (isTablet(context)) return 32.0;
    return 64.0;
  }

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        DeviceType deviceType = DeviceType.mobile;
        if (constraints.maxWidth >= 1024) {
          deviceType = DeviceType.desktop;
        } else if (constraints.maxWidth >= 600) {
          deviceType = DeviceType.tablet;
        }
        return builder(context, constraints, deviceType);
      },
    );
  }
}
