##  @file StateMachineTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "StateMachine" Type
#
#   @TODO
#   High Priority:
#   - Refactor the test to use constants once the interface for the
#     'StateMachine' type becomes less volatile.
#   Low Priority:
#   - Update the parameters for the 'step' function node lambda expressions
#     based on changes in the 'StateMachine' class.
#   - Refactor the set-up procedure to allow for conditional construction
#     of graphs based on the testing function.

import unittest
import networkx as NX
import src
from src.StateMachine import *
from src.Event import *

##  Container class for the test suite that tests the functionality of the
#   "StateMachine" type.
class StateMachineTest( unittest.TestCase ):
    ### Testing Constants ###

    ##  The step that will be used as the time delta when automating steps on
    #   the test state machines.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        simple_graph = NX.DiGraph()
        simple_graph.add_node( "zero", step=lambda tt, dt: {"tt": tt, "dt": dt} )
        self._simple_machine = StateMachine( simple_graph )

        complex_graph = NX.DiGraph()
        complex_graph.add_node( "one", step=lambda tt, dt: 1 )
        complex_graph.add_node( "two", step=lambda tt, dt: 2 )
        complex_graph.add_edge( "one", "two", event=EventType.NOTIFY )
        complex_graph.add_edge( "two", "one", event=EventType.NOTIFY )
        self._complex_machine = StateMachine( complex_graph, "two" )

    def tearDown( self ):
        self._simple_machine = None
        self._complex_machine = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        self.assertEqual( self._simple_machine.get_current_state(), "zero",
            "Default state machine constructor improperly sets initial state." )
        self.assertEqual( self._simple_machine.get_idle_time(), 0.0,
            "Default state machine constructor improperly sets initial idle time." )


    def test_value_constructor( self ):
        self.assertEqual( self._complex_machine.get_current_state(), "two",
            "Value state machine constructor improperly sets initial state." )
        self.assertEqual( self._complex_machine.get_idle_time(), 0.0,
            "Value state machine constructor improperly sets initial idle time." )


    def test_singular_automate( self ):
        self._simple_machine.automate_step( StateMachineTest.TIME_DELTA )

        self.assertEqual( self._simple_machine.get_current_state(), "zero",
            "Automating a machine step doesn't retain the original state." )
        self.assertEqual( self._simple_machine.get_idle_time(),
            StateMachineTest.TIME_DELTA,
            "Automating a single machine step doesn't properly update idle time." )

        self._simple_machine.automate_step( StateMachineTest.TIME_DELTA )

        self.assertEqual( self._simple_machine.get_idle_time(),
            2.0 * StateMachineTest.TIME_DELTA,
            "Automating multiple machine steps doesn't properly update idle time." )

        sdelta = self._simple_machine.automate_step( StateMachineTest.TIME_DELTA )

        self.assertEqual( sdelta[ "tt" ], 3.0 * StateMachineTest.TIME_DELTA,
            "Step automation doesn't properly pass the total time value to the " +
            "state step function." )
        self.assertEqual( sdelta[ "dt" ], StateMachineTest.TIME_DELTA,
            "Step automation doesn't properly pass the delta time value to the " +
            "state step function." )


    def test_invalid_notify( self ):
        self._simple_machine.automate_step( StateMachineTest.TIME_DELTA )
        self._simple_machine.notify_of( Event(EventType.NOTIFY) )

        self.assertEqual( self._simple_machine.get_current_state(), "zero",
            "Invalidly notifying a machine w/o transitions doesn't retain state." )
        self.assertEqual( self._simple_machine.get_idle_time(),
            StateMachineTest.TIME_DELTA,
            "Invalidly notifying a machine w/o transitions doesn't reset idle time." )

        self._complex_machine.automate_step( StateMachineTest.TIME_DELTA )
        self._complex_machine.notify_of( Event(EventType.COLLISION) )

        self.assertEqual( self._complex_machine.get_current_state(), "two",
            "Invalidly notifying a machine w/ transitions doesn't retain state." )
        self.assertEqual( self._simple_machine.get_idle_time(),
            StateMachineTest.TIME_DELTA,
            "Invalidly notifying a machine w/ transitions doesn't retain idle time." )


    def test_valid_notify( self ):
        self._complex_machine.automate_step( StateMachineTest.TIME_DELTA )
        self._complex_machine.notify_of( Event(EventType.NOTIFY) )

        self.assertEqual( self._complex_machine.get_current_state(), "one",
            "Validly notifying a machine to transition doesn't initiate proper " +
            "machine transition." )
        self.assertEqual( self._simple_machine.get_idle_time(), 0.0,
            "Validly notifying a machine to transition doesn't reset the idle " +
            "time for the machine." )


    def test_multistate_automate( self ):
        self._complex_machine.notify_of( Event(EventType.NOTIFY) )
        self._complex_machine.notify_of( Event(EventType.NOTIFY) )
        sdelta1 = self._complex_machine.automate_step( StateMachineTest.TIME_DELTA )

        self.assertEqual( sdelta1, 2,
            "Automating steps on a multistate machine causes an improper state " +
            "step function to be called." )

        self._complex_machine.notify_of( Event(EventType.NOTIFY) )
        sdelta2 = self._complex_machine.automate_step( StateMachineTest.TIME_DELTA )

        self.assertEqual( sdelta2, 1,
            "Automating steps on a multistate machine causes an improper state " +
            "step function to be called." )
