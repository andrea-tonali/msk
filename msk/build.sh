set -e

echo Build Docker
docker build --no-cache -t etls-denormalize-patient-journey -f etls/etls.Dockerfile .