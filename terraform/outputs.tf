output "travis_airmozilla_access_secret_key" {
  description = "Access key for Travis Airmozilla user"
  value = aws_iam_access_key.travis_airmozilla.secret
}

output "travis_airmozilla_access_key" {
  description = "Secret key for Travis Airmozilla user"
  value = aws_iam_access_key.travis_airmozilla.id
}
