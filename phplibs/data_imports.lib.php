<?php

function CSVToArray(array $aResult, array $aChamps, $iNbHeaders = 1, $cSeparator = "\t")
{
	$aData = array();
	foreach($aResult as $iLine => $aLine) {
		if($iLine >= $iNbHeaders) {
			$a = array();
			if(is_string($aLine)) $aLine = explode($cSeparator, $aLine);
			foreach($aLine as $id => $sValue) {
				if($sValue === 'NULL') $a[$aChamps[$id]] = NULL;
				else $a[$aChamps[$id]] = str_replace("\n", " ", $sValue);
			}
			$aData[] = $a;
		}
	}
	return $aData;
}

function LoadCSV($pathCSV, $iIgnoreHeadersLines = 0)
{
	$iNbHeaders = 1;
	$cSeparator = ',';

	$aLines = array();
	$f = fopen($pathCSV, 'r');
	$nbLine = 1;
	while($a = fgetcsv($f, 0, $cSeparator)) {
		if($nbLine > $iIgnoreHeadersLines) $aLines[] = $a;
		$nbLine++;
	}

	#$aLines = file($pathCSV);
	$aChamps = $aLines[0];
	unset($aLines[0]);

	foreach($aChamps as $id => & $sChamp) {
		$sChamp = iconv('UTF-8', 'ASCII//TRANSLIT', $sChamp);
		$sChamp = trim(preg_replace('/[^a-zA-Z0-9_]/', '_', $sChamp), '_');
		if(empty($sChamp)) $sChamp = 'inconnu'.$id;
	}
	return CSVToArray($aLines, $aChamps, $iNbHeaders, $cSeparator);
}

function DumpTableViaSSH($sServeur, $sTable, array $aChamps, $sWhere = '', $iNbHeaders = 1)
{
	if( ! empty($sWhere)) $sWhere = " WHERE $sWhere ";
	$sExec = "ssh %s 'mysql -e \"select %s from %s%s\"'";
	$sExec = sprintf($sExec, $sServeur, implode(',', $aChamps), $sTable, $sWhere);
	$s = exec($sExec, $aResult, $iResult);
	if($iResult == 0) {
		return CSVToArray($aResult, $aChamps, $iNbHeaders, "\t");
	}
	else die("erreur ($iResult) : " . implode(' / ', $aResult) . "\n");
}
