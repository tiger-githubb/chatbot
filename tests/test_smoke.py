#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de fumée rapide pour vérifier que l'application démarre
Test ultra-minimaliste pour les vérifications rapides
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def smoke_test():
    """Test de fumée : vérifie juste que l'application peut démarrer"""
    try:
        print("🔍 Import de main...")
        import main
        
        # Vérifier que l'app existe
        if hasattr(main, 'app'):
            print("✅ Application FastAPI OK")
            return True
        else:
            print("❌ Application FastAPI non trouvée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de fumée: {e}")
        return False


if __name__ == "__main__":
    print("🔥 Test de fumée...")
    result = smoke_test()
    if result:
        print("🎉 Test de fumée réussi !")
        sys.exit(0)
    else:
        print("💥 Test de fumée échoué !")
        sys.exit(1)
