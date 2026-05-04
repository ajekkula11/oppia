# Copyright 2024 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Facade for email-sending operations (630:P3 Issue #33).

Centralises the server_can_send_emails guard so that callers do not
need to reach into platform_parameter_services directly.  Before this
facade existed, every controller that wanted to send an email had to
repeat the same three-line platform-parameter lookup (Shotgun Surgery).
Now they call EmailFacade.can_send_emails() instead.
"""

from __future__ import annotations

from core.domain import platform_parameter_list
from core.domain import platform_parameter_services


class EmailFacade:
    """Facade that simplifies email availability checks for controllers.

    Provides a single, stable interface over the underlying
    platform_parameter_services so that controllers are decoupled from
    the detail of how the server-can-send-emails flag is stored and
    retrieved.
    """

    @staticmethod
    def can_send_emails() -> bool:
        """Returns True if the server is configured to send emails.

        Returns:
            bool. Whether the SERVER_CAN_SEND_EMAILS platform parameter
            is currently enabled.
        """
        return platform_parameter_services.get_platform_parameter_value(
            platform_parameter_list.ParamName.SERVER_CAN_SEND_EMAILS.value
        )
