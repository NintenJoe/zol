##  @file StateTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "State" Type
#
#   @TODO
#   - Update the 'TestStates' reference in this testing file once the location
#     of this file changes.

import unittest
import src
from TestStates import *
from src.SimulationDelta import *
from src.PhysicalState import *

##  Container class for the test suite that tests the functionality of the
#   "State" type.
class StateTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The string name identifier given to the testing state.
    STATE_NAME = "test"

    ##  The floating-point time out time for the testing state.
    STATE_TIMEOUT = 1.0

    ##  The floating-point time step that will be used for state step testing.
    STATE_TIMESTEP = 0.2

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._state = SimpleTestState( StateTests.STATE_NAME, StateTests.STATE_TIMEOUT )

        for i in range( int(StateTests.STATE_TIMEOUT / StateTests.STATE_TIMESTEP)-1 ):
            self._state.simulate_step( StateTests.STATE_TIMESTEP )

    def tearDown( self ):
        self._state = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_state = SimpleTestState( StateTests.STATE_NAME )

        self.assertEqual( default_state.get_name(), StateTests.STATE_NAME,
            "Default constructor improperly initializes the state name." )
        self.assertEqual( default_state.get_active_time(), 0.0,
            "Default constructor improperly initializes the state active time." )
        self.assertEqual( default_state.get_timeout_time(), float("inf"),
            "Default constructor improperly initializes state timeout time." )


    def test_value_constructor( self ):
        value_state = SimpleTestState( StateTests.STATE_NAME, StateTests.STATE_TIMEOUT )

        self.assertEqual( value_state.get_name(), StateTests.STATE_NAME,
            "Value constructor improperly initializes the state name." )
        self.assertEqual( value_state.get_active_time(), 0.0,
            "Value constructor improperly initializes the state active time." )
        self.assertEqual( value_state.get_timeout_time(), StateTests.STATE_TIMEOUT,
            "Value constructor improperly initializes state timeout time." )


    def test_step_before_timeout( self ):
        self.assertEqual( self._state.simulate_step( StateTests.STATE_TIMESTEP ),
            SimpleTestState.STEP_DELTA,
            "Pre-timeout step function returns an incorrect simulation delta." )
        self.assertAlmostEqual( self._state.get_active_time(),
            5 * StateTests.STATE_TIMESTEP, 5,
            "Pre-timeout step function improperly updates the state's active time." )


    def test_step_after_timeout( self ):
        self._state.simulate_step( StateTests.STATE_TIMESTEP )

        self.assertEqual( self._state.simulate_step( StateTests.STATE_TIMESTEP ),
            SimulationDelta(),
            "Post-timeout step function returns an incorrect simulation delta." )
        self.assertAlmostEqual( self._state.get_active_time(),
            6 * StateTests.STATE_TIMESTEP, 5,
            "Post-timeout step function improperly updates the state's active time." )

    def test_arrival( self ):
        arrival_delta = self._state.simulate_arrival()

        self.assertEqual( arrival_delta, SimpleTestState.ARRIVAL_DELTA,
            "Arrival function improperly returns the subclass simulation delta." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Arrival function doesn't properly reset the active time for the state." )


    def test_departure( self ):
        departure_delta = self._state.simulate_departure()

        self.assertEqual( departure_delta, SimpleTestState.DEPARTURE_DELTA,
            "Departure function improperly returns the subclass simulation delta." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Departure function doesn't properly reset the active time for the state." )


    def test_excess_time( self ):
        self.assertAlmostEqual( self._state.get_excess_time(), 0.0, 5,
            "Pre-timeout excess time calculation returns a non-zero value." )

        self._state.simulate_step( StateTests.STATE_TIMESTEP )
        self.assertAlmostEqual( self._state.get_excess_time(), 0.0, 5,
            "On-timeout excess time calculation returns a non-zero value." )

        self._state.simulate_step( StateTests.STATE_TIMESTEP )
        self.assertAlmostEqual( self._state.get_excess_time(),
            StateTests.STATE_TIMESTEP, 5,
            "Post-timeout excess time calculation returns an imporper value." )

