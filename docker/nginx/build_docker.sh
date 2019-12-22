{ # try
  mkdir .ssh
  cp ~/.ssh/id_rsa .ssh/id_rsa
  docker build -f Dockerfile -t tourist-nginx:latest .

} || { # catch
  echo "exception occurred"
}
rm -rf .ssh