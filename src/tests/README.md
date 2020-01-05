# Tests doc

Code flaw type|Code flaw | Tests link | Tests num | Additional
--- | --- | --- | --- | ---
switch|[#17][i17]|[link](test_game.py#L6-L54)|12
conditional complexity|[#7][i7]| - | - | Поскольку код с недостатком находится внутри бесконечного цикла и опирается на эвенты клавиатуры и мыши, написать юнит тест не представляется возможным
data clump|[#18][i18]|[link](test_interface.py#L7-L41)|8|Использованы mock'и
lazy class|[#28][i28]| - | - | Использование ленивого класса находится внутри огромного бесконечного цикла, поэтому написать юнит тесты не получается


[i7]: https://github.com/merry-cooperation/refactorMeowHero/issues/7
[i17]: https://github.com/merry-cooperation/refactorMeowHero/issues/17
[i18]: https://github.com/merry-cooperation/refactorMeowHero/issues/18
[i28]: https://github.com/merry-cooperation/refactorMeowHero/issues/28