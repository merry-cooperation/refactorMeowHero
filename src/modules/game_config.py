from .objects import Children, Dog, DancingCat, CatBossEnemy

# level number: (enemy spawn probability, enemy name parameter, enemy class)
ENEMY_CONFIG = {
    2: (1, "Children", Children),
    3: (0.9, "Dog", Dog),
    8: (0.42, "DancingCat", DancingCat),
    11: (0.2, "CatBossEnemy", CatBossEnemy)
}
