
namespace WolvenKit.RED4.Types
{
	public partial class gamedataVehicleAppearancesToColorTemplate_Record
	{
		[RED("colorTemplates")]
		[REDProperty(IsIgnored = true)]
		public CArray<TweakDBID> ColorTemplates
		{
			get => GetPropertyValue<CArray<TweakDBID>>();
			set => SetPropertyValue<CArray<TweakDBID>>(value);
		}
	}
}
