import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import boto3

from pydantic.env_settings import BaseSettings, deep_update, env_file_sentinel


ssm_client = boto3.client('ssm')

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

    @property
    def _ssm_client(self):
        return ssm_client

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _ssm_client: Any = None,
        _env_file: Union[Path, str, None] = None,
        _env_file_encoding: Optional[str] = None,
        _yaml_file: Union[Path, str, None] = None,
        _yaml_file_encoding: Optional[str] = None,
    ) -> Dict[str, Any]:
        built_dict_from_yaml_and_environ: dict = deep_update(
            self._build_environ(_env_file, _env_file_encoding),
            self._build_yaml_settings(_yaml_file, _yaml_file_encoding)
        )
        built_with_default_ssm_configs: dict = deep_update(
            built_dict_from_yaml_and_environ, self._read_ssm_config("default")
        )
        built_with_stage_ssm_configs: dict = deep_update(
            built_with_default_ssm_configs, self._read_ssm_config(os.environ["STAGE"])
        )
        return deep_update(built_with_stage_ssm_configs, init_kwargs)

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

    def _read_ssm_config(self, stage: str) -> dict:
        result = self._ssm_client.get_parameters_by_path(
            Path=f"/{stage}", Recursive=True, WithDecryption=True
        )

        config = {}
        for param in result["Parameters"]:
            option = config
            path = param["Name"].split("/")
            for p in path[2:-1]:
                option = option.setdefault(p, {})
            option[path[-1]] = param["Value"]

        return config

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
