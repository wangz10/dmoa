"""Handles most database transactions. It has knowledge of the primary classes
and their relationships and saves them accordingly.
"""

import sqlalchemy as sa

from substrate import BioCategory, Curator, GeneList, GeneSignature, \
    GeoDataset, Report, SoftFile, Tag

from gen3va.database.utils import session_scope


def count(class_):
    """Returns the number of rows in an class's associated table.
    """
    with session_scope() as session:
        return session.query(class_).count()


def get(class_, value, key='id'):
    """Gets entity by comparing column to value.
    """
    with session_scope() as session:
        return session\
            .query(class_)\
            .filter(getattr(class_, key) == value)\
            .first()


def get_many(klass, values, key='id'):
    """Gets entities whose column values are in values.
    """
    with session_scope() as session:
        return session\
            .query(klass)\
            .filter(getattr(klass, key).in_(values))\
            .all()


def get_all(klass):
    """Gets all entities of a specific class.
    """
    with session_scope() as session:
        return session.query(klass).all()


def get_signatures_by_ids(extraction_ids):
    """Returns all gene signatures with matching extraction IDs.
    """
    with session_scope() as session:
        return session\
            .query(GeneSignature)\
            .filter(GeneSignature.extraction_id.in_(extraction_ids))\
            .all()


def add_object(obj):
    """Create new object.
    """
    with session_scope() as session:
        session.add(obj)


def update_object(obj):
    """Update object, i.e. saves any edits.
    """
    with session_scope() as session:
        session.merge(obj)


def delete_object(obj):
    """Deletes object provided.
    """
    with session_scope() as session:
        session.delete(obj)


def get_tags_by_curator(curator):
    """Returns all tags by a particular curator
    """
    with session_scope() as session:
        return session\
            .query(Tag)\
            .filter(Tag.curator_fk == Curator.id)\
            .filter(Curator.name == curator)\
            .all()


def get_bio_categories():
    """Returns all bio categories which have tags from particular curators.
    """
    with session_scope() as session:
        return session\
            .query(BioCategory)\
            .order_by(BioCategory.order)\
            .all()


def get_bio_categories_by_curator(curator):
    """Returns all bio categories which have tags from particular curators.
    """
    with session_scope() as session:
        return session\
            .query(BioCategory)\
            .filter(BioCategory.id == Tag.bio_category_fk)\
            .filter(Curator.id == Tag.curator_fk)\
            .filter(Curator.name == curator)\
            .all()


def get_statistics():
    """Returns object with DB statistics for about page.
    """
    with session_scope() as session:
        meta_counts = session\
            .execute("""SELECT `name`, COUNT(DISTINCT `value`) AS `count`
                FROM `optional_metadata` 
                WHERE `name` IN ('cell', 'dose', 'time') 
                GROUP BY `name`""")\
            .fetchall()
        meta_counts = dict(meta_counts)    

        cell_counts = session\
            .execute("""SELECT `value`, COUNT(`value`) AS `count` 
                FROM `optional_metadata` 
                WHERE `name`='cell' 
                GROUP BY `value`
                """)\
            .fetchall()
        cell_counts = [{'cell': item[0], 'count': item[1]} for item in cell_counts]

        return {
            'num_gene_signatures': count(GeneSignature),
            'num_reports': count(Report),
            'num_cells': meta_counts['cell'],
            'num_doses': meta_counts['dose'],
            'num_times': meta_counts['time'],
            'cell_counts': cell_counts
        }

def get_all_drug_meta():
    """Returns a dict {pert_id: pert_iname} for all the drugs.
    """
    with session_scope() as session:
        d_pert_name = session\
            .execute("""SELECT `pert_id`, `pert_iname` 
                FROM `drug`
                """)\
            .fetchall()
        d_pert_name = dict(d_pert_name)

        return d_pert_name
