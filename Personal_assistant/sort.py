import shutil
import pathlib

sorted_files = {}
found_extension = set()
unknown_extension = set()


def sort_files(path, dest_dirs, work_extension, path_to_sort_folder):
    """
    Sorts files by folders in a destination directory depending on the file extension.
    """
    for path_element in pathlib.Path(path).iterdir():
        if path_element.is_dir() and path_element.name not in dest_dirs:
            sort_files(path_element, dest_dirs, work_extension, path_to_sort_folder)
            if not any(path_element.iterdir()):
                pathlib.Path(path_element).chmod(0o777)
                pathlib.Path(path_element).rmdir()

        elif path_element.suffix.upper() in work_extension['video']:
            try:
                shutil.move(path_element, rf'{path_to_sort_folder}\video')
                found_extension.add(path_element.suffix)
                sorted_files.setdefault('video', []).append(path_element.name)
            except shutil.Error as error:
                print(f"File move error: {error}")

        elif path_element.suffix.upper() in work_extension['images']:
            try:
                shutil.move(path_element, rf'{path_to_sort_folder}\images')
                found_extension.add(path_element.suffix)
                sorted_files.setdefault('images', []).append(path_element.name)
            except shutil.Error as error:
                print(f"File move error: {error}")

        elif path_element.suffix.upper() in work_extension['audio']:
            try:
                shutil.move(path_element, rf'{path_to_sort_folder}\audio')
                found_extension.add(path_element.suffix)
                sorted_files.setdefault('audio', []).append(path_element.name)
            except shutil.Error as error:
                print(f"File move error: {error}")

        elif path_element.suffix.upper() in work_extension['documents']:
            try:
                shutil.move(path_element, rf'{path_to_sort_folder}\documents')
                found_extension.add(path_element.suffix)
                sorted_files.setdefault('documents', []).append(path_element.name)
            except shutil.Error as error:
                print(f"File move error: {error}")

        elif path_element.suffix.upper() in work_extension['archives']:
            try:
                shutil.unpack_archive(path_element, fr'{path_to_sort_folder}\archives\{path_element.stem}')
                pathlib.Path(path_element).unlink()
                found_extension.add(path_element.suffix)
                sorted_files.setdefault('archives', []).append(path_element.name)
            except shutil.Error as error:
                print(f"File move / unpack error: {error}")

        else:
            path_element.suffix != '' and unknown_extension.add(path_element.suffix)


def output_sort_information():
    """
    Prints out a summary of the sort_files function call.
    """
    if sorted_files:
        print(f'The script sorted the files: {sorted_files}')
        print(f'The script sorted the files with extensions: {found_extension}')
    if unknown_extension:
        print(f'The script did not sort files with unknown extensions: {unknown_extension}')


def main():
    """
    The main function that performs file sorting and prints out the summary.
    The files are sorted by folders in a destination directory depending on extensions.
    """
    path_to_sort_folder = input("Enter the path to the folder you want to sort: ")

    dest_dirs = ['images', 'video', 'audio', 'documents', 'archives']
    work_extension = {'images': ('.JPEG', '.PNG', '.JPG', '.SVG'),
                      'video': ('.AVI', '.MP4', '.MOV', '.MKV'),
                      'audio': ('.MP3', '.OGG', '.WAV', '.AMR'),
                      'documents': ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
                      'archives': ('.ZIP', '.GZ', '.TAR')}

    # check if there are folders 'images', 'video', 'audio', 'documents', 'archives'
    # in the folder to be sorted. If these folders are missing, they are created
    for folder in dest_dirs:
        if not pathlib.Path(fr'{path_to_sort_folder}\{folder}').exists():
            pathlib.Path(fr'{path_to_sort_folder}\{folder}').mkdir()

    sort_files(path_to_sort_folder, dest_dirs, work_extension, path_to_sort_folder)
    output_sort_information()

    return ""


if __name__ == '__main__':
    main()
