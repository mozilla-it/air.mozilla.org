resource "aws_ecr_repository" "airmozilla" {
  name = "airmozilla"
}

resource "aws_ecr_lifecycle_policy" "keep_last_30" {
  repository = aws_ecr_repository.airmozilla.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep last 30 images",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 30
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

resource "aws_iam_user" "travis_airmozilla" {
	# This users is used for pushing containers from Travis to ECR
  name = "travis-airmozilla"
  path = "/airmozilla/"
}

resource "aws_iam_user_policy" "travis_airmozilla" {
  name  = "allow-${aws_iam_user.travis_airmozilla.name}-allow-access-to-ecr"
  user  = aws_iam_user.travis_airmozilla.name

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_access_key" "travis_airmozilla" {
  user = aws_iam_user.travis_airmozilla.name
}

resource "aws_ecr_repository_policy" "allow_travis_airmozilla_rw" {
  repository = aws_ecr_repository.airmozilla.name

  policy = <<EOF
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
              "AWS": "${aws_iam_user.travis_airmozilla.arn}"
            },
            "Action": [
							  "ecr:GetAuthorizationToken",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:DescribeRepositories",
                "ecr:GetRepositoryPolicy",
                "ecr:ListImages",
                "ecr:BatchDeleteImage"
            ]
        }
    ]
}
EOF
}
