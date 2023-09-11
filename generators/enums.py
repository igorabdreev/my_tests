"""Классы для хранения названий полей, которые можно получить из Keycloak и PersonProfile"""
from collections import namedtuple
from enum import Enum

Key = namedtuple('Key', ['jpe', 'segment'])
Segment = namedtuple('Segment', ['name', 'jpe'])


class KeycloakGen(Enum):
    """Названия полей, которые можно получить из Keycloak"""
    company_id = 'company-id'
    sf_id = 'sf-id'
    email = 'email'
    employee_id = 'employee-id'
    family_name = 'family_name'
    fio = 'name'
    login = 'preferred_username'
    person_id = 'person-id'
    tenant_id = 'tenant-id'


class PersonGen(Enum):
    """Названия полей, которые можно получить из PersonProfile"""
    _uuid_jpe = '$.data[0].uuid'
    _data_jpe = '$.data[0].data.'

    _j_basic = Segment(name='J.BASIC', jpe=_data_jpe)
    _j_contacts_external_email = Segment(name='J.CONTACTS.EXTERNALEMAIL', jpe=_data_jpe)
    _j_contacts_interoffice_email = Segment(name='J.CONTACTS.INTEROFFICEEMAIL', jpe=_data_jpe)
    _j_contacts_interoffice_tel = Segment(name="J.CONTACTS.INTEROFFICETEL", jpe=_data_jpe)
    _j_contacts_company_email = Segment(name="J.CONTACTS.COMPANYEMAIL", jpe=_data_jpe)
    _j_position = Segment(name='J.POSITION', jpe=f'{_data_jpe}position[0].')

    _p_basic = Segment(name='P.BASIC', jpe=_data_jpe)
    _p_basic_photo = Segment(name='P.BASIC.PHOTO', jpe=_data_jpe)
    _p_contacts_mobile = Segment(name="P.CONTACTS.MOBILE", jpe=_data_jpe)

    j_basic_uuid = Key(jpe=_uuid_jpe, segment=_j_basic.name)
    employee_id = Key(jpe=f'{_data_jpe}.employeeId', segment=_j_basic.name)

    j_contacts_external_email_uuid = Key(jpe=_uuid_jpe, segment=_j_contacts_external_email.name)
    j_contacts_company_email = Key(jpe=f'{_j_contacts_company_email.jpe}value', segment=_j_contacts_company_email.name)
    sigma_email = Key(jpe=f'{_j_contacts_external_email.jpe}value', segment=_j_contacts_external_email.name)

    j_contacts_interoffice_email_uuid = Key(jpe=_uuid_jpe, segment=_j_contacts_interoffice_email.name)
    alpha_email = Key(jpe=sigma_email.jpe, segment=_j_contacts_interoffice_email.name)

    j_contacts_interoffice_tel_uuid = Key(jpe=_uuid_jpe, segment=_j_contacts_interoffice_tel.name)
    office_phone = Key(jpe=f'{_data_jpe}phones[?(@.priority == true)].phone', segment=_j_contacts_interoffice_tel.name)

    j_position_uuid = Key(jpe=_uuid_jpe, segment=_j_position.name)
    mass = Key(jpe=f'{_j_position.jpe}mass', segment=_j_position.name)
    position_id = Key(jpe=f'{_j_position.jpe}positionId', segment=_j_position.name)

    p_basic_uuid = Key(jpe=_uuid_jpe, segment=_p_basic.name)
    fullname = Key(jpe=f'{_p_basic.jpe}fullName', segment=_p_basic.name)
    firstname = Key(jpe=f'{_p_basic.jpe}firstName', segment=_p_basic.name)
    lastname = Key(jpe=f'{_p_basic.jpe}lastName', segment=_p_basic.name)
    midname = Key(jpe=f'{_p_basic.jpe}midName', segment=_p_basic.name)

    p_basic_photo_uuid = Key(jpe=_uuid_jpe, segment=_p_basic_photo.name)
    photo_url = Key(jpe=f'{_p_basic_photo.jpe}url', segment=_p_basic_photo.name)
    photo_hash = Key(jpe=f'{_p_basic_photo.jpe}hash', segment=_p_basic_photo.name)

    p_contacts_mobile_uuid = Key(jpe=_uuid_jpe, segment=_p_contacts_mobile.name)
    mobile_phone = Key(jpe=sigma_email.jpe, segment=_p_contacts_mobile.name)


class OrgstructureGen(str, Enum):
    """Названия полей, которые можно передать в OrgStructure"""
    oshs = 'OSHS'
    sbergile = 'SBERGILE'
    up = 'UP'
    down = 'DOWN'


class OrgstructureDataPathGen(str, Enum):
    """Названия полей, которые можно получить из OrgStructure"""
    id = '.id'
    name = '.name'
    be_cod = '.data.beCode'
    be_name = '.data.beName'
    id_company = '.company'
    func_block_id = '.data.funcBlockId'
    func_block_name = '.data.funcBlock'
