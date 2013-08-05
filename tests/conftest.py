# -*- coding: utf-8 -*-
import moar
import pytest


@pytest.fixture(params=['PILEngine', 'WandEngine'])
def engine(request):
    return getattr(moar, request.param)()
