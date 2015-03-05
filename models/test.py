from models.db import session
from models.base import Affiliation, SubAffiliation

results = session.query(Affiliation).all()

print results

for result in results:
    print result.module_cost
    print result.name
    print "Fixed XP:", result.fixed_xp

    sub_affiliation = session.query(SubAffiliation).filter(SubAffiliation.id == result.sub_affiliation).one()
    print 'Sub Affiliation:', sub_affiliation.name
    print "Fixed XP:", sub_affiliation.fixed_xp


