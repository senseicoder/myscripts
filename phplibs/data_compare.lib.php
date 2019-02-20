<?php

function AnalysesSQL($oDB, array $aAnalyses, $bDebug = FALSE)
{
	foreach($aAnalyses as $sLib => $sSQL) if( ! empty($sSQL)) {
		$aResult = $oDB->Query($sSQL);
		if(count($aResult)) {
			$aDisplay = array();
			foreach($aResult as $aRec) $aDisplay[] = ' * ' . trim($aRec['lib']);
			if($bDebug) printf("=== SQL: %s\n", $sSQL);
			printf("%s :\n%s\n", $sLib, implode("\n", $aDisplay));
		}
	}
}

function RecodagesSQL($oDB, array $aAnalyses)
{
	foreach($aAnalyses as $sSQL) {
		$oDB->Exec($sSQL);
	}
}