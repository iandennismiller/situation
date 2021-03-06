#!/bin/bash
# based on https://github.com/Homebrew/brew/blob/master/docs/Python-for-Formula-Authors.md#installing
# rebuild with 'make homebrew'

PKG=situation

source $(brew --prefix)/bin/virtualenvwrapper.sh

if [ ! -z $VIRTUAL_ENV ]; then
    echo "run 'deactivate' since this will not work inside virtualenv"
    exit 1
fi

echo "one moment..."
python - <<EOF
import urllib2, codecs, json
name = "situation"
url = "https://pypi.io/pypi/{}/json".format(name)
f = urllib2.urlopen(url)
reader = codecs.getreader("utf-8")
pkg_data = json.load(reader(f))
f.close()
print(pkg_data["releases"].keys())
EOF
echo "If the latest version is listed above, Press ENTER."
echo "Otherwise, use ctrl-c to exit."
read ok

# create virtualenv and install
mktmpenv
cd ~/Work/${PKG}
make install

# use poet to build pip package manifest
pip install homebrew-pypi-poet
poet ${PKG} > /tmp/poet.rb

# extract python package URL
URL=$(perl -n000e 'print $1 while /^..resource\s\"situation\"\sdo\n\s+url\s\"(.*?)\"\n.*?\n..end\n\n/mg' /tmp/poet.rb)

# remove package resource from poet manifest
perl -0777 -i.original -pe 's/..resource\s\"situation\"\sdo\n.*?\n.*?\n..end\n\n//igs' /tmp/poet.rb

# determine sha256 checksum for python package
curl -q -o /tmp/pkg.tgz ${URL}
SHA=$(shasum -a 256 /tmp/pkg.tgz | cut -d ' ' -f 1 -)
rm /tmp/pkg.tgz

# write header
cat > /tmp/pkg.rb <<-EOF
# Homebrew Formula
# situation, Ian Dennis Miller
# rebuild with 'make homebrew'

class situation < Formula
  desc "Situation Modeling Language is an ontology for describing social situations."
  homepage "https://github.com/iandennismiller/situation"
  url "${URL}"
  sha256 "${SHA}"

EOF

# write poet manifest
cat /tmp/poet.rb >> /tmp/pkg.rb

# write footer
cat >> /tmp/pkg.rb <<-EOF

  include Language::Python::Virtualenv

  def install
    virtualenv_install_with_resources
  end
end
EOF

# exit virtualenv
deactivate

# finalize
mv /tmp/pkg.rb /tmp/${PKG}.rb
echo "created /tmp/${PKG}.rb"
