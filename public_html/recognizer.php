<?php

$words = array("hi", "I", "am", "Malia", "this", "app", "will", "help", "you", "to", "understand", "me", "better");

$word = $words[array_rand($words)];

header("Content-Type: application/json");
echo json_encode(array(
    "result" => array(
        "word" => $word
    )
));
