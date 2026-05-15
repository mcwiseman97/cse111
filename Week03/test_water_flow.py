from pytest import approx
import pytest

from water_flow import water_column_height, pressure_gain_from_water_height, pressure_loss_from_pipe, pressure_loss_from_fittings, reynolds_number, pressure_loss_from_pipe_reduction


def test_water_column_height():
    i = 0
    while i < 4:
        tower_height = [0.0, 0.0, 25.0, 48.3]
        tank_height = [0.0, 10.0, 0.0, 12.8]
        expected_hight = [0.0, 7.5, 25.0, 57.9]
        assert water_column_height(tower_height[i], tank_height[i]) == expected_hight[i]
        i += 1

def test_pressure_gain_from_water_height():
    height = [0.0, 30.2, 50.0]
    answer = [0.00, 295.628, 489.450]
    i = 0
    while i < 3:
        assert pressure_gain_from_water_height(height[i]) == approx(answer[i], abs=0.001)
        i += 1

def test_pressure_loss_from_pipe():
    pipe_diameter = [0.048692, 0.048692, 0.048692, 0.048692, 0.048692, 0.286870, 0.286870]
    pipe_length = [0.00, 200.00, 200.00, 200.00, 200.00, 1000.00, 1800.75]
    friction_factor = [0.018, 0.000,0.018, 0.018, 0.018, 0.013, 0.013]
    fluid_velocity = [1.75, 1.75, 0.00, 1.75, 1.65,1.65, 1.65]
    answer = [0.000, 0.000, 0.000, -113.008, -100.462, -61.576, -110.884]
    i = 0
    while i < 7:
        assert pressure_loss_from_pipe(pipe_diameter[i], pipe_length[i], friction_factor[i], fluid_velocity[i]) == approx(answer[i], abs=0.001)
        i += 1

def test_pressure_loss_from_fittings():
    fluid_velocity = [0.00, 1.65, 1.65, 1.75, 1.75]
    quantity_fittings = [3, 0, 2, 2, 5]
    answer = [0.000, 0.000, -0.109, -0.122, -0.306]
    i = 0
    while i < 5:
        assert pressure_loss_from_fittings(fluid_velocity[i], quantity_fittings[i]) == approx(answer[i], abs=0.001)
        i += 1

def test_reynolds_number():
    hydraulic_diameter = [0.048692, 0.048692, 0.048692, 0.286870, 0.286870]
    fluid_velocity = [0.00, 1.65, 1.75, 1.65, 1.75]
    answer = [0, 80069, 84922, 471729, 500318]
    i = 0
    while i < 5:
        assert reynolds_number(hydraulic_diameter[i], fluid_velocity[i]) == approx(answer[i], abs=1)
        i += 1

def test_pressure_loss_from_pipe_reduction():
    larger_diameter = [0.28687, 0.28687, 0.28687]
    fluid_velocity = [0.00, 1.65, 1.75]
    reynolds_number = [1, 471729, 500318]
    smaller_diameter = [0.048692, 0.048692, 0.048692]
    answer = [0.000, -163.744, -184.182]
    i = 0
    while i < 3:
        assert pressure_loss_from_pipe_reduction(larger_diameter[i], fluid_velocity[i], reynolds_number[i], smaller_diameter[i]) == approx(answer[i], abs=0.001)
        i += 1


# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])


