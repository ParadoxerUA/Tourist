{ # try
  mkdir .ssh
  cp ~/.ssh/id_rsa .ssh/id_rsa
  docker build -f Dockerfile -t tourist-celery:latest .

} || { # catch
  echo "exception occurred"
}
rm -rf .ssh