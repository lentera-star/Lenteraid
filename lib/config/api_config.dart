import 'package:flutter/foundation.dart';

/// API Configuration for Backend Services
class ApiConfig {
  // VPS Backend URL - Update this with your actual VPS IP or domain
  static const String _vpsUrl = 'http://YOUR_VPS_IP:8000';
  static const String _productionUrl = 'https://api.lenteradreamflow.com';
  
  // Use VPS URL in debug mode, production URL in release mode
  static String get baseUrl => kDebugMode ? _vpsUrl : _productionUrl;
  
  // API Endpoints
  static String get chatEndpoint => '$baseUrl/api/chat';
  static String get healthEndpoint => '$baseUrl/health';
  static String get audioEndpoint => '$baseUrl/api/audio/process';
  
  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Headers
  static Map<String, String> get defaultHeaders => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      };
}
