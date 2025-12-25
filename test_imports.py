#!/usr/bin/env python3
"""Quick test script for Tajaa CLI."""

import sys
sys.path.insert(0, '.')

print("=" * 50)
print("TAJAA CLI - Test Script")
print("=" * 50)

try:
    print("\n[1] Testing core.database...")
    from core.database import DatabaseManager
    print("    ✓ DatabaseManager imported")

    print("\n[2] Testing core.engine...")
    from core.engine import AsyncEngine
    print("    ✓ AsyncEngine imported")

    print("\n[3] Testing core.intelligence...")
    from core.intelligence import FuzzySearchEngine, ContextSuggestionEngine
    print("    ✓ Intelligence modules imported")

    print("\n[4] Testing core.plugin...")
    from core.plugin import PluginLoader, PluginRegistry
    print("    ✓ Plugin system imported")

    print("\n[5] Testing core.session...")
    from core.session import SessionManager
    print("    ✓ SessionManager imported")

    print("\n[6] Testing core.ui...")
    from core.ui import TajaaUI, CinematicIntro
    print("    ✓ UI components imported")

    print("\n[7] Testing main imports...")
    from main import VERSION, AUTHOR, TOOL_COUNT, TajaaCLI
    print(f"    ✓ Tajaa CLI v{VERSION} by {AUTHOR}")
    print(f"    ✓ {TOOL_COUNT}+ tools ready")

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED! ✓")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

