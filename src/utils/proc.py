from typing import Union, Any, List, Tuple

def safe_access_to_array(
    array:      List[Any],
    index:      int = 0,
    err_return: Any = ''
) -> Union[Any, str]:
    try:
        return array[index]
    except IndexError:
        return err_return
