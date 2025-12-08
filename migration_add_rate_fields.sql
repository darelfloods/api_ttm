-- Migration pour ajouter les nouveaux champs à la table rates
-- Date: 2025-12-08
-- Description: Ajout des champs pour la personnalisation des offres (image, badge, popularité, ordre, activation)

-- Ajouter les nouvelles colonnes à la table rates
ALTER TABLE rates ADD COLUMN IF NOT EXISTS image_url VARCHAR(255);
ALTER TABLE rates ADD COLUMN IF NOT EXISTS badge_icon VARCHAR(100);
ALTER TABLE rates ADD COLUMN IF NOT EXISTS badge_text VARCHAR(100);
ALTER TABLE rates ADD COLUMN IF NOT EXISTS is_popular BOOLEAN DEFAULT FALSE NOT NULL;
ALTER TABLE rates ADD COLUMN IF NOT EXISTS display_order INTEGER DEFAULT 0 NOT NULL;
ALTER TABLE rates ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE NOT NULL;

-- Mettre à jour les données existantes avec des valeurs par défaut
UPDATE rates SET is_popular = FALSE WHERE is_popular IS NULL;
UPDATE rates SET display_order = 0 WHERE display_order IS NULL;
UPDATE rates SET is_active = TRUE WHERE is_active IS NULL;

-- Exemple de données pour tester (optionnel)
-- UPDATE rates SET image_url = '/assets/offre1.png', is_popular = TRUE WHERE libelle = 'standard';
-- UPDATE rates SET badge_icon = 'fas fa-crown', badge_text = 'VIP', display_order = 1 WHERE libelle = 'elite';
-- UPDATE rates SET badge_icon = 'fas fa-fire', badge_text = 'Top Deal', display_order = 2 WHERE libelle = 'pro';

-- Vérifier les modifications
SELECT * FROM rates;
