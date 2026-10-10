KG=~/tutorenv/bin/kaggle; B=~/tutor/kaggle
$KG models create -p $B/model || echo "МОДЕЛЬ: возможно, уже существует"
$KG models instances create -p $B/tf && echo "KAGGLE TRANSFORMERS OK"
$KG models instances create -p $B/gguf && echo "KAGGLE GGUF OK"
echo "KAGGLE ОЧЕРЕДЬ ЗАВЕРШЕНА"
