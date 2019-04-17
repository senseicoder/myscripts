<?php

$aResult = array();
$a = array();

foreach(file($argv[1]) as $sLine) {
	$sLine = trim($sLine);

	#8
	#Mars 2017, Mer.
	#09:00 à 18:00
	#build OSEA
	#Cedric Girard, Accepté
	if(preg_match('/^[0-9]+$/', $sLine, $aMatch)) {
		if(! empty($a)) {
			$aResult[] = implode(';', $a);
			$a = array();
		}
	}

	#lundi, 13 mars 2017
	if(preg_match('/^[a-zA-Z]+, [0-9]+ [a-zA-Zéù]+ [0-9]+$/', $sLine, $aMatch)) {
		if(! empty($a)) {
			$aResult[] = implode(';', $a);
			$a = array();
		}
	}
	
	$a[] = $sLine;
}

$aResult[] = implode(';', $a);
echo implode("\n", $aResult);