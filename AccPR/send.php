//Определяем место сохранения загруженного файла и его имя
$destination = $_SERVER['DOCUMENT_ROOT']. '/uploads';
$fileTempName = $_FILES['parameter']['tmp_name'];

if (is_uploaded_file($fileTempName)) {
    //Проверяем тип файла и меняем его имя в соответствии
    $newFilename = $destination .'/user';

    switch ($_FILES['parameter']['type']) {
        case 'application/pdf':
            $newFilename .= '-document.pdf';
            break;

        case 'video/mp4':
            $newFilename .= '-video.mp4';
            break;

        default:
            echo 'Файл неподдерживаемого типа';
            exit;
    }

    //Перемещаем файл из временной папки в указанную
    if (move_uploaded_file($fileTempName, $newFilename)) {
        echo 'Файл сохранен под именем '. $newFilename;

    } else {
        echo 'Не удалось осуществить сохранение файла';
    }
} else {
    echo 'Файл не был загружен на сервер';
}