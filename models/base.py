from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from models.db import Base, engine

class Affiliation( Base ):
    __tablename__ = 'affiliation'
    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )
    description         = Column( String( 500 ), nullable=False, default='' )
    module_cost         = Column( Integer )
    primary_language    = Column( Integer, ForeignKey( 'languages.id' ))
    secondary_language  = Column( Integer, ForeignKey( 'languages.id' ))
    sub_affiliation = Column( Integer, ForeignKey( 'subaffiliation.id' ))


    # This contain serialized information JSON or serialized dict
    fixed_xp        = Column( String( 2000 ), nullable=False )


class SubAffiliation( Base ):
    __tablename__ = 'subaffiliation'
    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )
    description         = Column( String( 500 ), nullable=False, default='' )

    # This contain serialized information JSON or serialized dict
    fixed_xp        = Column( String( 2000 ), nullable=False )


class Attribute( Base ):
    __tablename__ = 'attribute'

    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )

class Trait( Base ):
    __tablename__ = 'trait'
    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )
    description = Column( String( 500 ), nullable=False, default='' )


class Skill( Base ):
    __tablename__ = 'skill'

    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )
    description = Column( String( 500 ), nullable=False, default='' )


class Languages( Base ):
    __tablename__ = 'languages'

    id      = Column( Integer, primary_key=True )
    name    = Column( String( 50 ), nullable=False )


Base.metadata.create_all( engine )
