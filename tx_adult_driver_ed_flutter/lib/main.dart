import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'config/theme.dart';
import 'providers/auth_provider.dart';
import 'providers/course_provider.dart';
import 'services/storage_service.dart';
import 'views/landing/landing_page.dart';
import 'views/classroom/classroom_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await StorageService.init();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()..initAuth()),
        ChangeNotifierProvider(create: (_) => CourseProvider()..loadCurriculum()),
      ],
      child: const TexasAdeApp(),
    ),
  );
}

class TexasAdeApp extends StatelessWidget {
  const TexasAdeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Texas Adult Driver Education (ADE-1317)',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const LandingPage(),
        '/classroom': (context) => const ClassroomScreen(),
      },
    );
  }
}
