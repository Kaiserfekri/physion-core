def test_li_metal_interface_not_trivial():
    from physion_core.physics.interface import current_density
    i = current_density(eta=0.05, i0=1.0, alpha=0.5, T=298)
    assert i != 0.05 / 1.0

def test_sei_growth_non_linear():
    from physion_core.fullcell.sei import sei_growth_rate
    r1 = sei_growth_rate(i=1.0)
    r2 = sei_growth_rate(i=2.0)
    assert r2 > 2 * r1
