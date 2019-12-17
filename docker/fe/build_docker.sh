{ # try
  mkdir .ssh
  cp ~/.ssh/id_rsa .ssh/id_rsa
  docker build -f Dockerfile -t tourist-fe:latest .

} || { # catch
  echo "exception occurred"
}
rm -rf .ssh