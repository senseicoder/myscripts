<?php

function AnalysesSQL($oDB, array $aAnalyses)
{
	foreach($aAnalyses as $sLib => $sSQL) if( ! empty($sSQL)) {
		$aResult = $oDB->Query($sSQL);
		if(count($aResult)) {
			$aDisplay = array();
			foreach($aResult as $aRec) $aDisplay[] = ' * ' . trim($aRec['lib']);
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