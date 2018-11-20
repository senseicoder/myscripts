<?php

function AnalysesSQL($oDB, array $aAnalyses)
{
	foreach($aAnalyses as $sLib => $sSQL) if( ! empty($sSQL)) {
		$aResult = $oDB->Query($sSQL);
		if(count($aResult)) {
			$aDisplay = array();
			foreach($aResult as $aRec) $aDisplay[] = trim($aRec['lib']);
			printf("%s : %s\n", $sLib, implode(', ', $aDisplay));
		}
	}
}