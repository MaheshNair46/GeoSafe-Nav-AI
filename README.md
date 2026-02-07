GeoSafe-Nav: Dynamic Curve Safety AssistantA Physics-Based Voice Guidance Enhancement for GPS Navigation

📌 OverviewCurrent navigation systems focus on legal speed limits. This project proposes a Physics-Based Safety Layer that calculates the maximum safe entry speed for upcoming road curves based on real-time geometry and centrifugal force limits.

🚀 Key FeaturesCurvature Analysis: Uses 3-point GPS coordinate clusters to calculate the radius of a curve.Physics Engine: Applies the centripetal force formula ($v = \sqrt{\mu g r}$) to determine the safe velocity threshold.Proactive Voice AI: Integrated Text-to-Speech (TTS) to provide real-time coaching: "Slow down to 45 km/h for the upcoming sharp turn.

🛠 Technical ImplementationLanguage: Python 3.xLibraries: math, pyttsx3Geospatial Logic: Haversine formula for point-to-point distance and Heron’s formula for circumcircle radius calculation.

💡 The VisionI am proposing this as an enhancement for platforms like Google Maps. By moving beyond static speed limits and toward dynamic, geometry-aware safety alerts, we can significantly reduce run-off-road (ROR) accidents on unfamiliar routes.
