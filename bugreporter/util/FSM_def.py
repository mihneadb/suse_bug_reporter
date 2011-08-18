# FSM_def.py - a class definition module for suse bug reporting tool for the
# Finite State Machine used to get bug data from the user
#
# Copyright (C) 2009 Novell Inc.
# Author: Michal Vyskocil <mvyskocil@suse.cz>
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.

__version__ = '0.1'


import sys
import logging


logging.basicConfig()
log = logging.getLogger('bugreporter')


class FSM(object):
    """Finite State Machine implementation. It could be used for implementing
    of an interactive workflow, without a mess with complicated conditions.
    This class is intended to be subclassed and cannot be used directly.
    
    States are implemented in do_STATE methods and every method have to
    return a name of previous STATE, or a tuple (STATE, kwargs), which will be
    used as a keyword arguments for a next state. The default prefix `do_' is
    controlled by class variable PREFIX and could be changed. If state method
    returns None, it will cause a StopIteration error, which stops a
    transitions. If returns a non existing state, it the do_ERROR with an error
    wil be called.

    Instances of FSM subclass looks like iterable objects, because it provides
    a functions __iter__ and next(), so the easiest way how to run over all
    states is for state in fsm: pass and this is exactly what method main()
    does. In fact main method takes care about error states too.
    """

    PREFIX="do_"
    END_STATES=("ERROR", "EXIT")

    def __init__(self):
        """Initialize instance variables _kwargs and _state"""

        self._kwargs = {}
        self._state = "START"

    def dispatch(self, name):
        """Return a callable for given state name"""
        log.debug("STATE: %s" % name)
        return getattr(self, "%s%s" % (self.__class__.PREFIX, name))

    def filter_kwargs(self, callable, kwargs):
        """Return a dictionary only with arguments, which should be passed to
        callable"""
        ret = {}
        varnames = callable.im_func.func_code.co_varnames
        for k in [k for k in kwargs if k != 'self' and k in varnames]:
            ret[k] = kwargs[k]
        return ret

    def call(self, callable, **kwargs):
        """Call callable with given keyword arguments and return the (STATE,
        kwargs) tuple. If callable return None, it raises a StopIteration"""
        i = callable(**kwargs)
        if i == None:
            raise StopIteration
        if type(i) == str:
            return (i, {})
        else:
            return (i[0], i[1])

    def next(self):
        """Do a transition - get a callable from dispatch, filter keyword args,
        so only defined will be passed to a method, call it and check a return
        state"""
        callable = self.dispatch(self._state)
        kwargs = self.filter_kwargs(callable, self._kwargs)
        self._state, self._kwargs = self.call(callable, **kwargs)
        return self._state

    def main(self):
        """A main loop. Iterates for all states and catches errors during
        transtion. On every error, it will setup the state to ERROR and add an
        error message.

        1.) If some function returns a non-existing state
        2.) If loop ends and state is not in END_STATES
        """
        try:
            for state in self:
                pass
        except AttributeError, ae:
            self._state = "ERROR"
            self._kwargs = {'message' : "Transition error: %s" % (ae, )}
            self.next()
        if self._state not in self.__class__.END_STATES:
            self._kwargs = {'message' : "Transition error: %s ends in a state `%s'" % (self, self._state)}
            self._state = "ERROR"
            self.next()

        return self

    def __iter__(self):
        return self

    def do_START(self):
        """A default start method. This one raises a NotImplementedError"""
        raise NotImplementedError("This has to be reimplemented in a subclass!!")
    
    def do_ERROR(self, message="Error", exit=1):
        """A default error handler. It prints a message to stderr and exits with exit code."""
        print >>sys.stderr, message
        sys.exit(exit)
        return None
    
    def do_EXIT(self):
        """A default exit handler"""
        return None
