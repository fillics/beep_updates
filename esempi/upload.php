<?php
$target_dir = "uploads/"; // Cartella di destinazione files
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$fileExtension = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

// ## FILE VALIDATION ##
// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
  echo "ERRORE: Dimensione file troppo elevata\n\n";
  $uploadOk = 0;
}

// Permettiamo solo specifiche estensioni
if($fileExtension != "txt" && $fileExtension != "dat" && $fileExtension != "pkl") {
  echo "ERRORE: Estensione file non valida.\nPosso accettare solo .txt o .dat o .pkl\n\n";
  $uploadOk = 0;
}

if ($uploadOk == 0) {
  echo "Il file NON è stato caricato\n";
} else { //se non ho riscontrato problemi, prova a caricare
  if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    echo "\nIl File ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " è stato caricato.\n";
  } else {
    echo "\nERRORE: C'è stato un problema non definito durante il salvataggio del file.\n";
  }
}


?>
