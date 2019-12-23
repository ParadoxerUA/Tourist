{ # try
  mkdir .ssh
  cp ~/.ssh/id_rsa .ssh/id_rsa
  docker build --no-cache=true -f Dockerfile -t tourist-be:latest .

} || { # catch
  echo "exception occurred"
}
rm -rf .ssh