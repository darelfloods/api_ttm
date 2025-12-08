"""
Script de migration pour ajouter les nouveaux champs à la table rates
Date: 2025-12-08
Usage: python migrate_database.py
"""

from app.Db.Connection import engine, Base
from app.Db.Model.RateModel import Rate
from sqlalchemy import inspect, text

def check_column_exists(table_name, column_name):
    """Vérifie si une colonne existe dans une table"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate():
    """Exécute la migration de la base de données"""
    print("🔄 Début de la migration de la base de données...")
    
    try:
        # Créer toutes les tables avec les nouveaux champs
        # SQLAlchemy ajoutera automatiquement les colonnes manquantes
        Base.metadata.create_all(bind=engine)
        
        print("✅ Migration réussie !")
        print("\nNouveaux champs ajoutés à la table 'rates':")
        print("  - image_url (VARCHAR)")
        print("  - badge_icon (VARCHAR)")
        print("  - badge_text (VARCHAR)")
        print("  - is_popular (BOOLEAN)")
        print("  - display_order (INTEGER)")
        print("  - is_active (BOOLEAN)")
        
        # Vérifier que les colonnes ont été ajoutées
        print("\n🔍 Vérification des colonnes...")
        new_columns = ['image_url', 'badge_icon', 'badge_text', 'is_popular', 'display_order', 'is_active']
        
        for col in new_columns:
            exists = check_column_exists('rates', col)
            status = "✅" if exists else "❌"
            print(f"{status} {col}: {'Présent' if exists else 'Absent'}")
        
        print("\n✨ Migration terminée avec succès !")
        print("\nProchaines étapes:")
        print("1. Redémarrez l'API backend")
        print("2. Testez l'ajout d'une offre depuis l'interface admin")
        print("3. Vérifiez que les offres s'affichent correctement sur le site public")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        raise

if __name__ == "__main__":
    migrate()
