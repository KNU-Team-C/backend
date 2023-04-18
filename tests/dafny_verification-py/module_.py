import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_
import _dafny
import System_

assert "module_" == __name__
module_ = sys.modules[__name__]

class Company:
    def  __init__(self):
        self.id: int = int(0)
        self.name: _dafny.Seq = _dafny.Seq({})
        self.email: _dafny.Seq = _dafny.Seq({})
        self.address: _dafny.Seq = _dafny.Seq({})
        self.phone__number: _dafny.Seq = _dafny.Seq({})
        self.employees__num: int = int(0)
        self.logo__url: _dafny.Seq = _dafny.Seq({})
        self.mini__logo__url: _dafny.Seq = _dafny.Seq({})
        self.location: _dafny.Seq = _dafny.Seq({})
        self.description: _dafny.Seq = _dafny.Seq({})
        self.is__blocked: bool = False
        self.is__verified: bool = False
        self.date__created: _dafny.Seq = _dafny.Seq({})
        pass

    def __dafnystr__(self) -> str:
        return "_module.Company"
    def ctor__(self, id, name, email, address, phone__number, employees__num, logo__url, mini__logo__url, location, description, is__blocked, is__verified, date__created):
        (self).id = id
        (self).name = name
        (self).email = email
        (self).address = address
        (self).phone__number = phone__number
        (self).employees__num = employees__num
        (self).logo__url = logo__url
        (self).mini__logo__url = mini__logo__url
        (self).location = location
        (self).description = description
        (self).is__blocked = is__blocked
        (self).is__verified = is__verified
        (self).date__created = date__created


class Program:
    def  __init__(self):
        self.companies: _dafny.Seq = _dafny.Seq({})
        pass

    def __dafnystr__(self) -> str:
        return "_module.Program"
    def ctor__(self):
        (self).companies = _dafny.SeqWithoutIsStrInference([])

    def isUnique(self, s):
        res: bool = False
        hi0_: int = len(self.companies)
        for d_0_i_ in range(0, hi0_):
            if ((self.companies)[d_0_i_].name) == (s.name):
                res = False
                return res
        res = True
        return res
        return res

    def LastIndexOf(self, c, s):
        index: int = int(0)
        index = -1
        hi1_: int = len(s)
        for d_1_i_ in range(0, hi1_):
            if ((s)[d_1_i_]) == (c):
                index = d_1_i_
        return index

    def NumberOfChars(self, c, s):
        num: int = int(0)
        num = 0
        hi2_: int = len(s)
        for d_2_i_ in range(0, hi2_):
            if ((s)[d_2_i_]) == (c):
                num = (num) + (1)
        return num

    def IsValidEmail(self, email):
        valid: bool = False
        d_3_atIndex_: int
        out0_: int
        out0_ = (self).LastIndexOf(_dafny.CodePoint('@'), email)
        d_3_atIndex_ = out0_
        d_4_dotIndex_: int
        out1_: int
        out1_ = (self).LastIndexOf(_dafny.CodePoint('.'), email)
        d_4_dotIndex_ = out1_
        d_5_aNum_: int
        out2_: int
        out2_ = (self).NumberOfChars(_dafny.CodePoint('@'), email)
        d_5_aNum_ = out2_
        valid = (((((d_3_atIndex_) >= (0)) and ((d_4_dotIndex_) > (d_3_atIndex_))) and ((d_4_dotIndex_) < ((len(email)) - (1)))) and ((d_5_aNum_) == (1))) and ((len(email)) > (3))
        return valid

    def add__company(self, name, email, address, phone__number, employees__num, logo__url, mini__logo__url, location, description):
        company: module_.Company = None
        unique: bool = False
        created: bool = False
        validEmail: bool = False
        nw0_ = module_.Company()
        nw0_.ctor__((len(self.companies)) + (1), name, email, address, phone__number, employees__num, logo__url, mini__logo__url, location, description, False, False, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "date_created")))
        company = nw0_
        out3_: bool
        out3_ = (self).IsValidEmail(email)
        validEmail = out3_
        out4_: bool
        out4_ = (self).isUnique(company)
        unique = out4_
        if (unique) and (validEmail):
            (self).companies = (self.companies) + (_dafny.SeqWithoutIsStrInference([company]))
            created = True
        elif True:
            created = False
        return company, unique, created, validEmail


