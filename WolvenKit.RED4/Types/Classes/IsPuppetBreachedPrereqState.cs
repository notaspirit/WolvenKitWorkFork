using static WolvenKit.RED4.Types.Enums;

namespace WolvenKit.RED4.Types
{
	public partial class IsPuppetBreachedPrereqState : gamePrereqState
	{
		[Ordinal(0)] 
		[RED("psListener")] 
		public CHandle<gameScriptedPrereqPSChangeListenerWrapper> PsListener
		{
			get => GetPropertyValue<CHandle<gameScriptedPrereqPSChangeListenerWrapper>>();
			set => SetPropertyValue<CHandle<gameScriptedPrereqPSChangeListenerWrapper>>(value);
		}

		public IsPuppetBreachedPrereqState()
		{
			PostConstruct();
		}

		partial void PostConstruct();
	}
}
