from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic.env_settings import BaseSettings, deep_update, env_file_sentinel


yaml_file_sentinel = str(object())


class CustomSettings(BaseSettings):
    def __init__(
            self,
            _env_file: Union[Path, str, None] = env_file_sentinel,
            _env_file_encoding: Optional[str] = None,
            _yaml_file: Union[Path, str, None] = yaml_file_sentinel,
            _yaml_file_encoding: Optional[str] = None,
            **values: Any
    ) -> None:
        super().__init__(
            **self._build_values(
                values,
                _env_file=_env_file,
                _env_file_encoding=_env_file_encoding,
                _yaml_file=_yaml_file,
                _yaml_file_encoding=_yaml_file_encoding,
            )
        )

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _env_file: Union[Path, str, None] = None,
        _env_file_encoding: Optional[str] = None,
        _yaml_file: Union[Path, str, None] = None,
        _yaml_file_encoding: Optional[str] = None,
    ) -> Dict[str, Any]:
        built_dict_from_yaml_and_environ: dict = deep_update(
            self._build_environ(_env_file, _env_file_encoding),
            self._build_yaml_settings(_yaml_file, _yaml_file_encoding)
        )
        return deep_update(built_dict_from_yaml_and_environ, init_kwargs)

    def _build_yaml_settings(
            self, _yaml_file: Union[Path, str, None] = None, _yaml_file_encoding: Optional[str] = None,
    ) -> Dict[str, Optional[str]]:
        """
        Build settings from yaml file
        :param _yaml_file: yaml file with settings
        :param _yaml_file_encoding: yaml encoding
        :return: dict
        """
        yaml_vars: dict = {}
        yaml_file = _yaml_file if _yaml_file != yaml_file_sentinel else self.__config__.yaml_file
        if _yaml_file_encoding is not None:
            yaml_file_encoding: Optional[str] = _yaml_file_encoding
        else:
            yaml_file_encoding: str = self.__config__.yaml_file_encoding
        if yaml_file is not None:
            yaml_path: Path = Path(yaml_file)
            if yaml_path.is_file():
                yaml_vars: dict = {
                    **_read_yaml_file(
                        yaml_path, encoding=yaml_file_encoding, case_sensitive=self.__config__.case_sensitive
                    ),
                }
        return yaml_vars

    class Config:
        yaml_file = None
        yaml_file_encoding = None


def _read_yaml_file(
        file_path: Path, *, encoding: str = None, case_sensitive: bool = False
) -> Dict[str, Optional[str]]:
    import yaml

    file_vars: Dict[str, Optional[str]] = yaml.load(file_path.open(encoding=encoding), Loader=yaml.FullLoader)
    if not case_sensitive:
        return {k.lower(): v for k, v in file_vars.items()}
    else:
        return file_vars
