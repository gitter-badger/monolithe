# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import shutil

from monolithe.lib import Printer
from monolithe.generators.lib import Generator
from monolithe.generators.managers import MainManager, CLIManager, VanillaManager
from .sdkapiversiongenerator import SDKAPIVersionGenerator


class SDKGenerator(Generator):
    """
    """

    def cleanup(self):
        """
        """
        output = self.monolithe_config.get_option("output", "transformer")
        language = self.monolithe_config.language

        overrides_path = "%s/%s/__overrides" % (output, language)
        if os.path.exists(overrides_path):
            shutil.rmtree(overrides_path)

        attrs_defaults_path = "%s/%s/__attributes_defaults" % (output, language)
        if os.path.exists(attrs_defaults_path):
            shutil.rmtree(attrs_defaults_path)

        code_header_path = "%s/%s/__code_header" % (output, language)
        if os.path.exists(code_header_path):
            os.remove(code_header_path)

    def generate(self, specification_info):
        """
        """
        user_vanilla = self.monolithe_config.get_option("user_vanilla", "transformer")
        output = self.monolithe_config.get_option("output", "transformer")
        name = self.monolithe_config.get_option("name", "transformer")
        lang = self.monolithe_config.language

        vanilla_manager = VanillaManager(monolithe_config=self.monolithe_config)
        vanilla_manager.execute(output_path="%s/%s" % (output, lang))

        self.install_user_vanilla(user_vanilla_path=user_vanilla, output_path="%s/%s" % (output, lang))

        version_generator = SDKAPIVersionGenerator(monolithe_config=self.monolithe_config)
        apiversions = []

        for info in specification_info:
            Printer.log("transforming specifications into %s for version %s..." % (lang, info["api"]["version"]))
            apiversions.append(info["api"]["version"])

        version_generator.generate(specification_info=specification_info)

        Printer.log("assembling...")
        manager = MainManager(monolithe_config=self.monolithe_config)
        manager.execute(apiversions=apiversions)

        cli_manager = CLIManager(monolithe_config=self.monolithe_config)
        cli_manager.execute()

        self.cleanup()
        Printer.success("%s generation complete and available in \"%s/%s\"" % (name, output, self.monolithe_config.language))

    def generate_documentation(self):
        """
        """
        name = self.monolithe_config.get_option("name", "transformer")
        output = self.monolithe_config.get_option("output", "transformer")
        doc_output = self.monolithe_config.get_option("doc_output", "transformer")

        input_path = os.path.join(output, self.monolithe_config.language, name)
        output_path = os.path.join(doc_output, self.monolithe_config.language)

        if self.monolithe_config.language == 'python':
            Printer.log("generating documentation...")
            os.system("pdoc --overwrite --html --html-dir '%s' '%s' >/dev/null 2>&1" % (output_path, input_path))
            Printer.success("%s documentation generation complete and available in \"%s\"" % (name, output_path))
        else:
            Printer.warn("no documentation generator for this language. ignoring")
