<?php

function DumpTableViaSSH($sServeur, $sTable, array $aChamps, $sWhere = '', $iNbHeaders = 1)
{
	if( ! empty($sWhere)) $sWhere = " WHERE $sWhere ";
	$sExec = "ssh %s 'mysql -e \"select %s from %s%s\"'";
	$sExec = sprintf($sExec, $sServeur, implode(',', $aChamps), $sTable, $sWhere);
	$s = exec($sExec, $aResult, $iResult);
	if($iResult == 0) {
		$aData = array();
		foreach($aResult as $iLine => $sLine) {
			if($iLine >= $iNbHeaders) {
				$sLine = trim($sLine);
				$a = array();
				foreach(explode("\t", $sLine) as $id => $sValue) {
					if($sValue === 'NULL') $a[$aChamps[$id]] = NULL;
					else $a[$aChamps[$id]] = $sValue;
				}
				$aData[] = $a;
			}
		}
		return $aData;
	}
	else die("erreur ($iResult) : " . implode(' / ', $aResult) . "\n");
}
