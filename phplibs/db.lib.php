<?php

class CDB
{
	private $mysqli;

	function __construct($dbHost, $dbLogin, $dbPassword, $dbBase)
	{
		$this->mysqli = new mysqli($dbHost, $dbLogin, $dbPassword, $dbBase);
		if ($this->mysqli->connect_error) die('Erreur de connexion (' . $this->mysqli->connect_errno . ') ' . $mysqli->connect_error);
		$this->mysqli->set_charset("utf8");
	}

	function __destruct()
	{
		$this->mysqli->close();
	}

	function Exec($sSQL)
	{
		if($this->mysqli->query($sSQL) !== TRUE) {
			die(sprintf("erreur '%s' pour: %s\n", $this->mysqli->error, $sSQL));
		}		
	}

	function Query($sSQL)
	{
		if($result = $this->mysqli->query($sSQL)) {
			$aResult = array();
			while ($row = $result->fetch_assoc()) $aResult[] = $row;
			return $aResult;			
		}
		else {
			die(sprintf("erreur '%s' pour: %s\n", $this->mysqli->error, $sSQL));
		}
	}

	function Recreate($sTableName, array $aFields)
	{
		$this->Exec('drop table if exists ' . $sTableName);
		$sSQL = sprintf('create table %s(%s)', $sTableName, implode(',', $aFields));
		$this->Exec($sSQL);
	}

	function ReCreateDatabase($sDBName)
	{
		$this->Exec('drop database if exists ' . $sDBName);
		$sSQL = sprintf('create database %s', $sDBName);
		$this->Exec($sSQL);	
		$this->mysqli->select_db($sDBName);	
	}

	private function FormatArray(array $in, $sFormat, array $aChamps = array())
	{
		$aOut = array();
		if(empty($aChamps)) {
			foreach($in as $sValue) {
				$aOut[] = sprintf($sFormat, $sValue);
			}
		}
		else {
			foreach($aChamps as $sChamp) {
				$sValue = isset($in[$sChamp]) ? $in[$sChamp] : '';
				$aOut[] = sprintf($sFormat, $sValue);
			}
		}
		return $aOut;
	}

	function Table2Array($sNom)
	{
		return $this->Query("select * from $sNom");
	}

	function Array2Table($sNom, array $aData, array $aChamps = array())
	{
		if(empty($aChamps)) $aChamps = array_keys($aData[0]);
		$aChampsCreate = self::FormatArray($aChamps, '`%s` VARCHAR(255)');
		$aChampsList = self::FormatArray($aChamps, '`%s`');

		$nb = 0;
		$sTable = $sNom;
		$this->Recreate($sTable, $aChampsCreate);
		foreach($aData as $aLine) {
			$aValues = self::FormatArray($aLine, '"%s"', $aChamps);
			$this->Exec(sprintf('insert into %s(%s) values(%s)', $sTable, implode(',', $aChampsList), implode(',', $aValues)));
			$nb++;
		}		
		return $nb;
	}
}
