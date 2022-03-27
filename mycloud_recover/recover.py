import csv
import os
import sqlite3
import sys

from tqdm import tqdm


def file_count(conn):
    """
    Returns the total number of files in the db, ignores directories.
    """
    cur = conn.cursor()
    cur.execute(
        """
        select count(*)
        from files
        where mimeType != 'application/x.wd.dir'
        """
    )
    (file_count,) = cur.fetchone()
    return int(file_count)


def path_gen(conn):
    """
    Generates paths from the database.
    """
    cur = conn.cursor()
    resp = cur.execute(
        """
        select parentID,contentID,name
        from files
        where mimeType != 'application/x.wd.dir'
        """
    )
    for parent_id, content_id, name in resp:
        path = get_path_from_db(conn, parent_id, [name])
        if not content_id:
            continue
        yield content_id, path


def get_path_from_db(conn, parent_id, path):
    """
    Get the full path from the database.
    """
    cur = conn.cursor()
    cur.execute("select parentID,name from files where id = ?", (parent_id,))
    parent_id, name = cur.fetchone()
    path.append(name)
    if parent_id is None:
        return os.path.join(*reversed(path))
    return get_path_from_db(conn, parent_id, path)


def recover(db_path, content_dir, output_dir, verbose, no_write):
    """
    Recover a filesystem from a mycloud home database and file directory.
    """
    conn = sqlite3.connect(db_path)
    count = file_count(conn)
    recovered = 0
    missing_content = []
    for content_id, path in tqdm(path_gen(conn), total=count):
        content_path = os.path.join(content_dir, content_id[0], content_id)
        output_path = os.path.join(output_dir, path)
        content_exists = os.path.exists(content_path)
        output_exists = os.path.exists(output_path)
        if output_exists:
            continue
        if not content_exists:
            print(f"ERROR: Failed to find content at {content_path!r}", file=sys.stderr)
            missing_content.append(content_path)
            continue
        if verbose:
            print(f"Recovering {path!r} from content {content_id}")
        if not no_write:
            dirname = os.path.dirname(output_path)
            os.makedirs(dirname, exist_ok=True)
            os.rename(content_path, output_path)
            recovered += 1

    print(
        f"""
        Recovery completed:
            expected: {count}
            recovered: {recovered}
            missing content: {len(missing_content)}
        """
    )
    for f in missing_content:
        print(f"MISSING CONTENT: {f!r}")
