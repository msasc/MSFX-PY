#  Copyright (c) 2023 Miquel Sas.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from msfx.db.data import Types, Field, Table, Relation, View

f_CODE = Field()
f_CODE.set_name("MASTER")
f_CODE.set_type(Types.STRING)
f_CODE.set_length(40)

f_DESC = Field()
f_DESC.set_name("MASTER")
f_DESC.set_type(Types.STRING)
f_DESC.set_length(80)

f_CARTICLE = Field(f_CODE)
f_CARTICLE.set_name("CARTICLE")

f_DARTICLE = Field(f_DESC)
f_DARTICLE.set_name("DARTICLE")

f_CCOMPANY = Field(f_CODE)
f_CCOMPANY.set_name("CCOMPANY")

f_DCOMPANY = Field(f_DESC)
f_DCOMPANY.set_name("DCOMPANY")

f_QSALES = Field()
f_QSALES.set_name("QSALES")
f_QSALES.set_type(Types.DECIMAL)
f_QSALES.set_length(20)
f_QSALES.set_decimals(4)

f_NYEAR = Field()
f_NYEAR.set_name("NYEAR")
f_NYEAR.set_type(Types.DECIMAL)
f_NYEAR.set_length(4)
f_NYEAR.set_decimals(0)

f_NMONTH = Field()
f_NMONTH.set_name("NMONTH")
f_NMONTH.set_type(Types.DECIMAL)
f_NMONTH.set_length(2)
f_NMONTH.set_decimals(0)

t_ARTICLES = Table()
t_ARTICLES.set_name("ARTICLES")
t_ARTICLES.append_field(f_CARTICLE)
t_ARTICLES.append_field(f_DARTICLE)
t_ARTICLES.get_field("CARTICLE").set_primary_key(True)
t_ARTICLES.get_field("CARTICLE").set_persistent(True)
t_ARTICLES.get_field("DARTICLE").set_persistent(True)
t_ARTICLES.validate_and_setup()

print(t_ARTICLES.get_primary_key())

t_COMPANIES = Table()
t_COMPANIES.set_name("COMPANIES")
t_COMPANIES.append_field(f_CCOMPANY)
t_COMPANIES.append_field(f_DCOMPANY)
t_COMPANIES.get_field("CCOMPANY").set_primary_key(True)
t_COMPANIES.get_field("CCOMPANY").set_persistent(True)
t_COMPANIES.get_field("DCOMPANY").set_persistent(True)
t_COMPANIES.validate_and_setup()

print(t_COMPANIES.get_primary_key())

t_MSALES = Table()
t_MSALES.set_name("MSALES")
t_MSALES.append_field(f_CCOMPANY)
t_MSALES.append_field(f_CARTICLE)
t_MSALES.append_field(f_NYEAR)
t_MSALES.append_field(f_NMONTH)
t_MSALES.append_field(f_QSALES)
t_MSALES.get_field("CCOMPANY").set_primary_key(True)
t_MSALES.get_field("CARTICLE").set_primary_key(True)
t_MSALES.get_field("NYEAR").set_primary_key(True)
t_MSALES.get_field("NMONTH").set_primary_key(True)
t_MSALES.get_field("CCOMPANY").set_persistent(True)
t_MSALES.get_field("CARTICLE").set_persistent(True)
t_MSALES.get_field("NYEAR").set_persistent(True)
t_MSALES.get_field("NMONTH").set_persistent(True)
t_MSALES.get_field("QSALES").set_persistent(True)
t_MSALES.validate_and_setup()

print(t_MSALES.get_primary_key())

r_ARTICLES = Relation(t_MSALES, t_ARTICLES)
r_ARTICLES.add_segment(t_MSALES.get_field("CARTICLE"), t_ARTICLES.get_field("CARTICLE"))

r_COMPANIES = Relation(t_MSALES, t_COMPANIES)
r_COMPANIES.add_segment(t_MSALES.get_field("CCOMPANY"), t_COMPANIES.get_field("CCOMPANY"))

v_MSALES = View()
v_MSALES.set_master_table(t_MSALES)
v_MSALES.append_relation(r_COMPANIES)
v_MSALES.append_relation(r_ARTICLES)
v_MSALES.append_field(t_MSALES.get_field("CCOMPANY"))
v_MSALES.append_field(t_MSALES.get_field("CARTICLE"))
v_MSALES.append_field(t_MSALES.get_field("NYEAR"))
v_MSALES.append_field(t_MSALES.get_field("NMONTH"))
v_MSALES.append_field(t_MSALES.get_field("QSALES"))
v_MSALES.append_field(t_COMPANIES.get_field("DCOMPANY"))
v_MSALES.append_field(t_ARTICLES.get_field("DARTICLE"))
v_MSALES.append_order_by_field(t_MSALES.get_field("CCOMPANY"))
v_MSALES.append_order_by_field(t_MSALES.get_field("CARTICLE"))
v_MSALES.append_order_by_field(t_MSALES.get_field("NYEAR"))
v_MSALES.append_order_by_field(t_MSALES.get_field("NMONTH"))
v_MSALES.validate_and_setup()

print(v_MSALES.get_field("CARTICLE").is_foreign())
print(v_MSALES.get_field("DARTICLE").is_foreign())